import asyncio
import random
import time
from typing import Optional

from fastapi import FastAPI, Query, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(
    title="Demo API",
    description="SRE Platform Lab demo service with observability endpoints",
    version="1.0.0",
)

# Prometheus metrics
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

startup_time = time.time()


@app.get("/health")
async def health():
    """Liveness probe endpoint. Returns healthy if the process is running."""
    REQUEST_COUNT.labels(method="GET", endpoint="/health", status="200").inc()
    return {"status": "healthy"}


@app.get("/ready")
async def ready():
    """Readiness probe endpoint. Returns ready if the service can handle traffic."""
    uptime = time.time() - startup_time
    REQUEST_COUNT.labels(method="GET", endpoint="/ready", status="200").inc()
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

    start = time.time()
    await asyncio.sleep(delay)
    duration = time.time() - start

    REQUEST_LATENCY.labels(method="GET", endpoint="/simulate-latency").observe(duration)
    REQUEST_COUNT.labels(method="GET", endpoint="/simulate-latency", status="200").inc()

    return {
        "simulated_delay_seconds": round(delay, 3),
        "actual_duration_seconds": round(duration, 3),
    }


@app.get("/simulate-error")
async def simulate_error(
    rate: Optional[float] = Query(default=1.0, ge=0, le=1.0),
):
    """Simulate errors for testing alerting. Rate is probability of error (0.0 to 1.0)."""
    if random.random() < rate:
        ERROR_COUNT.labels(method="GET", endpoint="/simulate-error", status="500").inc()
        REQUEST_COUNT.labels(method="GET", endpoint="/simulate-error", status="500").inc()
        return Response(
            content='{"status": "error", "message": "Simulated internal server error"}',
            status_code=500,
            media_type="application/json",
        )

    REQUEST_COUNT.labels(method="GET", endpoint="/simulate-error", status="200").inc()
    return {"status": "ok", "message": "No error this time"}
