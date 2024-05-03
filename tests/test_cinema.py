import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_city(aclient: AsyncClient):

    response = await aclient.post("/create", json={"title": "test city"})

    assert response.status_code == 200
    assert response.json() == {"city": 1}
