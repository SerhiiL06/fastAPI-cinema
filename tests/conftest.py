import asyncio

import pytest
from src.infrastructure.database.connections import session_transaction
from httpx import ASGITransport, AsyncClient
from .database import test_session

from main import app


app.dependency_overrides[session_transaction] = test_session


@pytest.fixture(scope="session")
async def aclient():
    async with ASGITransport(app=app) as tr:
        aclient = AsyncClient(
            transport=tr,
            base_url="http://test",
        )
        yield aclient
