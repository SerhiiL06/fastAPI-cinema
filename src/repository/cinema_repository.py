from typing import Optional

from fastapi import HTTPException
from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.infrastructure.database.models.cinema import Cinema, City
from src.presentation.mappings.cinema import CinemaDTO, ShortCinemaDTO

from .abstract import AbstractRepository


class CityRepository:

    async def get_city_by_id(self, city_id, session: AsyncSession) -> Optional[City]:
        return await session.get(City, city_id)

    async def create_city(self, data: dict, session: AsyncSession) -> Optional[int]:

        query = insert(City).values(**data).returning(City.id)

        try:
            result = await session.execute(query)
            await session.commit()

            return result.scalar()
        except IntegrityError:
            raise HTTPException(400, "unique error")


class CinemaRepository(CityRepository, AbstractRepository):

    async def find_all(self, session: AsyncSession) -> list[Cinema]:
        query = select(Cinema).options(joinedload(Cinema.city))
        result = await session.execute(query)
        return result.scalars().all()

    async def create(self, cinema: Cinema, session: AsyncSession) -> int:
        city = await self.get_city_by_id(cinema.city_id, session)

        if city is None:
            raise HTTPException(404, "city with this id doesn't exists")

        cinema.city = city
        session.add(cinema)
        await session.commit()

        await session.refresh(cinema)

        return cinema.id

    async def find_by_id(self, entity_id: int, session: AsyncSession) -> Cinema:
        cinema = await session.get(Cinema, entity_id, options=[joinedload(Cinema.city)])

        if cinema is None:
            raise HTTPException(404, "cinema doesn't exists")

        return cinema

    def update(self, obj_id: int, data: dict):
        return super().update(obj_id, data)

    async def delete(self, obj_id: int, session: AsyncSession) -> None:
        query = await self.find_by_id(obj_id, session)

        await session.delete(query)
        await session.commit()
