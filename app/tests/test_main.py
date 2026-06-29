import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.anyio
async def test_ready():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "uptime_seconds" in data


@pytest.mark.anyio
async def test_metrics():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text


@pytest.mark.anyio
async def test_simulate_latency():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/simulate-latency?seconds=0.1")
    assert response.status_code == 200
    data = response.json()
    assert data["simulated_delay_seconds"] == 0.1
    assert data["actual_duration_seconds"] >= 0.1


@pytest.mark.anyio
async def test_simulate_error_guaranteed():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/simulate-error?rate=1.0")
    assert response.status_code == 500


@pytest.mark.anyio
async def test_simulate_error_no_error():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/simulate-error?rate=0.0")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
