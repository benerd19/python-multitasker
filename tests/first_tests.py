import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        response = await ac.post('/api/v1/users/', json={
            "name": "Test user",
            "email": "H4w4D@example.com",
            "password": "testpassword123",
            "avatar": "avatar"
        })

    assert response.status_code == 200
    data = response.json()
    assert "access" in data
