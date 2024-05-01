from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession

from src.presentation.mappings.cinema import CinemaDTO, CityDTO
from src.repository.cinema_repository import CinemaRepository
from src.repository.converters.cinema import (convert_cinema_dto_to_entity,
                                              convert_cinema_entity_to_dto)


class CinemaService:
    def __init__(self) -> None:
        self.repo = CinemaRepository()

    async def add_city(self, data: CityDTO, session: AsyncSession):

        city_id = await self.repo.create_city(asdict(data), session)

        return {"city": city_id}

    async def add_cinema(self, data: CinemaDTO, session: AsyncSession) -> dict:

        cinema_id = await self.repo.create(convert_cinema_dto_to_entity(data), session)

        return {"id": cinema_id}

    async def get_cinema_list(self, session: AsyncSession):
        entities = await self.repo.find_all(session)
        return convert_cinema_entity_to_dto(entities)

    async def get_cinema(self, entity_id: int, session: AsyncSession):
        cinema = await self.repo.find_by_id(entity_id, session)

        return cinema

    async def destroy_cinema(self, entity_id: int, session: AsyncSession):
        await self.repo.delete(entity_id, session)
