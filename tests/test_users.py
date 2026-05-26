import pytest
from httpx import AsyncClient


class TestUsers:
    @pytest.mark.asyncio
    async def test_read_current_user(
        self, client: AsyncClient, auth_headers: dict
    ):
        response = await client.get("/api/v1/users/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"

    @pytest.mark.asyncio
    async def test_read_current_user_unauthorized(self, client: AsyncClient):
        response = await client.get("/api/v1/users/me")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_update_current_user(
        self, client: AsyncClient, auth_headers: dict
    ):
        response = await client.patch(
            "/api/v1/users/me",
            json={"username": "updateduser"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["username"] == "updateduser"

    @pytest.mark.asyncio
    async def test_list_users_as_admin(
        self, client: AsyncClient, admin_headers: dict
    ):
        response = await client.get("/api/v1/users/", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    @pytest.mark.asyncio
    async def test_list_users_as_non_admin(
        self, client: AsyncClient, auth_headers: dict
    ):
        response = await client.get("/api/v1/users/", headers=auth_headers)
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_get_user_by_id(
        self, client: AsyncClient, admin_headers: dict
    ):
        response = await client.get("/api/v1/users/me", headers=admin_headers)
        user_id = response.json()["id"]
        response = await client.get(
            f"/api/v1/users/{user_id}", headers=admin_headers
        )
        assert response.status_code == 200
        assert response.json()["id"] == user_id

    @pytest.mark.asyncio
    async def test_get_user_not_found(
        self, client: AsyncClient, admin_headers: dict
    ):
        response = await client.get(
            "/api/v1/users/nonexistent-id", headers=admin_headers
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_admin_deletes_user(
        self, client: AsyncClient, admin_headers: dict
    ):
        response = await client.get("/api/v1/users/me", headers=admin_headers)
        user_id = response.json()["id"]
        response = await client.delete(
            f"/api/v1/users/{user_id}", headers=admin_headers
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_non_admin_cannot_delete(
        self, client: AsyncClient, auth_headers: dict
    ):
        response = await client.delete(
            "/api/v1/users/some-id", headers=auth_headers
        )
        assert response.status_code == 403
