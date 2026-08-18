import asyncio
import logging
import os
import random
import time
from typing import Optional

from fastapi import FastAPI, Query, Request, Response
from prometheus_client import Counter, Histogram, Info, generate_latest, CONTENT_TYPE_LATEST

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("demo-api")

app = FastAPI(
    title="Demo API",
    description="SRE Platform Lab demo service with observability endpoints",
    version="1.0.0",
)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

ERROR_COUNT = Counter(
    "http_errors_total",
    "Total HTTP errors",
    ["method", "endpoint", "status"],
)

APP_INFO = Info("demo_api", "Demo API build information")
APP_INFO.info({
    "version": "1.0.0",
    "environment": os.getenv("ENVIRONMENT", "local"),
})

startup_time = time.time()


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    if request.url.path in ("/health", "/ready", "/metrics"):
        return await call_next(request)

    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path,
    ).observe(duration)

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=str(response.status_code),
    ).inc()

    if response.status_code >= 500:
        ERROR_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=str(response.status_code),
        ).inc()

    return response


@app.get("/")
async def root():
    """Root endpoint with service info."""
    return {
        "service": "demo-api",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "local"),
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Liveness probe endpoint. Returns healthy if the process is running."""
    return {"status": "healthy"}


@app.get("/ready")
async def ready():
    """Readiness probe endpoint. Returns ready if the service can handle traffic."""
    uptime = time.time() - startup_time
    return {
        "status": "ready",
        "uptime_seconds": round(uptime, 2),
    }


@app.get("/metrics")
async def metrics():
    """Prometheus-compatible metrics endpoint."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.get("/simulate-latency")
async def simulate_latency(
    seconds: Optional[float] = Query(default=None, ge=0, le=30),
):
    """Simulate request latency for testing alerting and dashboards."""
    delay = seconds if seconds is not None else random.uniform(0.1, 3.0)
    await asyncio.sleep(delay)
    logger.info("Simulated latency: %.3fs", delay)
    return {
        "simulated_delay_seconds": round(delay, 3),
    }


@app.get("/simulate-error")
async def simulate_error(
    rate: Optional[float] = Query(default=1.0, ge=0, le=1.0),
):
    """Simulate errors for testing alerting. Rate is probability of error (0.0 to 1.0)."""
    if random.random() < rate:
        logger.warning("Simulated 500 error triggered")
        return Response(
            content='{"status": "error", "message": "Simulated internal server error"}',
            status_code=500,
            media_type="application/json",
        )

    return {"status": "ok", "message": "No error this time"}
