import re
from dataclasses import asdict

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.logic import clear_none
from src.infrastructure.database.models.cinema import Cinema
from src.presentation.mappings.cinema import CinemaDTO, CityDTO
from src.presentation.mappings.main import data_mapper
from src.repository.cinema_repository import CinemaRepository


class CinemaService:
    def __init__(self, repo: CinemaRepository) -> None:
        self.repo = repo

    async def add_city(self, data: CityDTO, session: AsyncSession):

        city_id = await self.repo.create_city(asdict(data), session)

        return {"city": city_id}

    async def add_cinema(self, data: CinemaDTO, session: AsyncSession) -> dict:

        validate_data = asdict(self.cinema_validate(data))
        cinema_id = await self.repo.create(
            data_mapper.load(validate_data, Cinema), session
        )

        return {"id": cinema_id}

    async def get_cinema_list(self, session: AsyncSession):
        cinema_list = await self.repo.find_all(session)
        cinema_list = data_mapper.dump(cinema_list, list[CinemaDTO])
        return {"cinemas_list": cinema_list}

    async def get_cinema(self, entity_id: int, session: AsyncSession):
        cinema = await self.repo.find_by_id(entity_id, session)

        return {"cinema": cinema}

    async def destroy_cinema(self, entity_id: int, session: AsyncSession):
        await self.repo.delete(entity_id, session)

    async def update_cinema(
        self, entity_id: int, data: CinemaDTO, session: AsyncSession
    ):

        cleared_data = clear_none(data)

        q = await self.repo.update(entity_id, cleared_data, session)

        return q

    @classmethod
    def cinema_validate(cls, dto: CinemaDTO):
        exception_list = {"errors": {}}

        if not re.findall(r"^\w+@example|gmail|mail.com", dto.email):
            exception_list["errors"]["email"] = "invalid email pattern"

        if not re.findall(r"\d{10}", dto.phone_number):
            exception_list["errors"]["phone_number"] = "invalid phone number pattern"

        if exception_list.get("errors"):
            raise HTTPException(400, exception_list)

        return dto
