import pytest
from .database import test_engine
from httpx import AsyncClient
from src.infrastructure.database.models.base import Base


@pytest.fixture()
async def up_db():
    async with test_engine.begin() as eng:
        await eng.run_sync(Base.metadata.create_all)
        yield
        await eng.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio(scope="session")
async def test_something(aclient: AsyncClient):
    response = await aclient.get("/cinema")

    assert response.status_code == 200
    assert response.json() == []
