from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession

from src.presentation.mappings.cinema import CinemaDTO, CityDTO
from src.repository.cinema_repository import CinemaRepository
from src.repository.converters.cinema import convert_cinema_dto_to_entity


class CinemaService:
    def __init__(self) -> None:
        self.repo = CinemaRepository()

    async def add_city(self, data: CityDTO, session: AsyncSession):

        city_id = await self.repo.create_city(asdict(data), session)

        return {"city": city_id}

    async def add_cinema(self, data: CinemaDTO, session: AsyncSession) -> dict:

        cinema_id = await self.repo.create(convert_cinema_dto_to_entity(data), session)

        return {"id": cinema_id}
