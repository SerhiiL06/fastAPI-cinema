import re
from dataclasses import asdict

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.presentation.mappings.cinema import CinemaDTO, CityDTO
from src.repository.cinema_repository import CinemaRepository
from src.repository.converters.cinema import (cinema_dto_to_entity,
                                              cinema_entity_to_dto)


class CinemaService:
    def __init__(self, repo: CinemaRepository) -> None:
        self.repo = repo

    async def add_city(self, data: CityDTO):

        city_id = await self.repo.create_city(asdict(data))

        return {"city": city_id}

    async def add_cinema(self, data: CinemaDTO) -> dict:

        validate_data = self.cinema_validate(data)
        cinema_id = await self.repo.create(cinema_dto_to_entity(validate_data))

        return {"id": cinema_id}

    async def get_cinema_list(self):
        entities = await self.repo.find_all()

        return {"cinemas_list": cinema_entity_to_dto(entities)}

    async def get_cinema(self, entity_id: int):
        cinema = await self.repo.find_by_id(entity_id)

        return {"cinema": cinema}

    async def destroy_cinema(self, entity_id: int):
        await self.repo.delete(entity_id)

    async def update_cinema(self, entity_id: int, data: CinemaDTO):

        cleared_data = self.clear_none(asdict(data))

        if not cleared_data:
            raise HTTPException(400, "No data to update")

        q = await self.repo.update(entity_id, cleared_data)

        return q

    @classmethod
    def cinema_validate(dto: CinemaDTO):
        exception_list = {"errors": {}}

        if not re.findall(r"^\w+@example|gmail|mail.com", dto.email):
            exception_list["errors"]["email"] = "invalid email pattern"

        if not re.findall(r"\d{10}", dto.phone_number):
            exception_list["errors"]["phone_number"] = "invalid phone number pattern"

        if exception_list.get("errors"):
            raise HTTPException(400, exception_list)

        return dto

    @classmethod
    def clear_none(cls, data: dict):
        after = {}
        for k, v in data.items():
            if v:
                after.update({k: v})

        return after
