import pytest
from fastapi import status
from httpx import AsyncClient, ASGITransport
from backend.app.main import app

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/health")
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == {"status":"ok"}

@pytest.mark.asyncio
async def test_chat():
    payload = {"message":"Qu'est-ce qu'un CDD ?"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.post("/chat", json=payload)
        assert r.status_code == status.HTTP_200_OK
        assert "response" in r.json()
        assert isinstance(r.json()["response"], str)
