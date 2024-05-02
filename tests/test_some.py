import pytest

from .database import test_engine
from src.infrastructure.database.models.base import Base
from httpx import AsyncClient
import asyncio


@pytest.mark.asyncio
async def test_create_city(aclient: AsyncClient):

    response = await aclient.post("/create", json={"title": "test city"})

    assert response.status_code == 200
    assert response.json() == 2


# @pytest.mark.asyncio
# async def test_create_cinema(aclient: AsyncClient):

#     response = await aclient.post("/cinema", json={"title": "test", "city_id": 1})

#     assert response.status_code == 200
