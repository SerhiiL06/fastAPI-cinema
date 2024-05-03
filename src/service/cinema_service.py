from dataclasses import asdict

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.presentation.mappings.cinema import CinemaDTO, CityDTO
from src.repository.cinema_repository import CinemaRepository
from src.repository.converters.cinema import (cinema_dto_to_entity,
                                              cinema_entity_to_dto)
from src.service.validators.cinema_validate import cinema_validate


class CinemaService:
    def __init__(self) -> None:
        self.repo = CinemaRepository()

    async def add_city(self, data: CityDTO, session: AsyncSession):

        city_id = await self.repo.create_city(asdict(data), session)

        return {"city": city_id}

    async def add_cinema(self, data: CinemaDTO, session: AsyncSession) -> dict:

        cinema_id = await self.repo.create(
            cinema_dto_to_entity(cinema_validate(data)), session
        )

        return {"id": cinema_id}

    async def get_cinema_list(self, session: AsyncSession):
        entities = await self.repo.find_all(session)
        return {"cinemas_list": cinema_entity_to_dto(entities)}

    async def get_cinema(self, entity_id: int, session: AsyncSession):
        cinema = await self.repo.find_by_id(entity_id, session)

        return {"cinema": cinema}

    async def destroy_cinema(self, entity_id: int, session: AsyncSession):
        await self.repo.delete(entity_id, session)

    async def update_cinema(
        self, entity_id: int, data: CinemaDTO, session: AsyncSession
    ):

        cleared_data = self.clear_none(asdict(data))

        if not cleared_data:
            raise HTTPException(400, "No data to update")

        q = await self.repo.update(entity_id, cleared_data, session)

        print(q)

        return q

    @classmethod
    def clear_none(cls, data: dict):
        after = {}
        for k, v in data.items():
            if v:
                after.update({k: v})

        return after
