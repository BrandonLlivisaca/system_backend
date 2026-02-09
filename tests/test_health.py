import pytest

@pytest.mark.anyio
async def test_health_endpoint(client):
    """Verificar que el endpoint de health funciona"""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

@pytest.mark.anyio
async def test_root_endpoint(client):
    """Verificar que el endpoint raiz funciona"""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data