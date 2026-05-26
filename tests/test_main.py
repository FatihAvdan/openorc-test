from httpx import AsyncClient, ASGITransport
import pytest

from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_item(client):
    response = await client.post(
        "/api/items",
        json={"name": "test item", "description": "a test"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test item"
    assert data["description"] == "a test"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_items(client):
    await client.post("/api/items", json={"name": "item1"})
    await client.post("/api/items", json={"name": "item2"})
    response = await client.get("/api/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


@pytest.mark.asyncio
async def test_get_item(client):
    create_resp = await client.post("/api/items", json={"name": "findme"})
    item_id = create_resp.json()["id"]
    response = await client.get(f"/api/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "findme"


@pytest.mark.asyncio
async def test_get_item_not_found(client):
    response = await client.get("/api/items/nonexistent")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_item(client):
    create_resp = await client.post("/api/items", json={"name": "delete me"})
    item_id = create_resp.json()["id"]
    response = await client.delete(f"/api/items/{item_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_item_not_found(client):
    response = await client.delete("/api/items/nonexistent")
    assert response.status_code == 404
