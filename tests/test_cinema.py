import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_city(aclient: AsyncClient):

    response = await aclient.post("/city", json={"title": "test city"})

    assert response.status_code == 200
    assert response.json() == {"city": 1}


# @pytest.mark.asyncio
# async def test_create_cinema(aclient: AsyncClient):
#     fake_cinema = {
#         "title": "test cinema",
#         "city_id": 1,
#         "street": "test street",
#         "house_number": 1,
#         "phone_number": "1234567890",
#         "description": "open every day",
#         "email": "testcinema@gmail.com",
#     }

#     response = await aclient.post("/cinemas", json=fake_cinema)

#     assert response.status_code == 204

#     fake_cinema["phone_number"] = "12"
#     fake_cinema["email"] = "test"

#     response = await aclient.post("/cinemas", json=fake_cinema)
#     assert response.status_code == 400
#     assert response.json()["detail"]["errors"] == {
#         "email": "invalid email pattern",
#         "phone_number": "invalid phone number pattern",
#     }


# @pytest.mark.asyncio
# async def test_list_of_cinema(aclient: AsyncClient):

#     response = await aclient.get("/cinemas")

#     assert response.status_code == 200
#     assert type(response.json()["cinemas_list"]) == list
#     assert response.json()["cinemas_list"][0]["id"] == 1


# @pytest.mark.asyncio
# async def test_retrieve_cinema(aclient: AsyncClient):

#     response = await aclient.get("/cinemas/1")

#     assert response.status_code == 200
#     assert bool(response.json()["cinema"]) == True
#     assert response.json()["cinema"]["id"] == 1


# @pytest.mark.asyncio
# async def test_update_cinema(aclient: AsyncClient):

#     response = await aclient.patch("/cinemas/1/update", json={"title": "updated_title"})

#     assert response.status_code == 200
#     assert response.json()[0]["title"] == "updated_title"

#     response = await aclient.patch("/cinemas/1/update", json={})
#     assert response.status_code == 400
#     assert response.json()["detail"] == "No data to update"


# @pytest.mark.asyncio
# async def test_drop_cinema(aclient: AsyncClient):

#     response = await aclient.delete("/cinemas/1/delete")

#     assert response.status_code == 204

#     response = await aclient.get("/cinemas/1")

#     assert response.status_code == 404
