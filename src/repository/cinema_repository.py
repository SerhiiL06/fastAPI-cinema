from typing import Optional

from fastapi import HTTPException
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.cinema import Cinema, City

from .abstract import AbstractRepository


class CityRepository:

    async def get_city_by_id(self, city_id, session: AsyncSession) -> Optional[City]:
        return await session.get(City, city_id)


class CinemaRepository(CityRepository, AbstractRepository):

    async def find_all(self, session: AsyncSession) -> list[Cinema]:
        query = select(Cinema)
        return await session.execute(query)

    async def create_city(self, data: dict, session: AsyncSession) -> Optional[int]:

        query = insert(City).values(**data).returning(City.id)

        try:
            result = await session.execute(query)
            await session.commit()

            return result.scalar()
        except IntegrityError:
            raise HTTPException(400, "unique error")

    async def create(self, cinema: Cinema, session: AsyncSession) -> int:
        city = await self.get_city_by_id(cinema.city_id, session)

        if city is None:
            raise HTTPException(404, "city with this id doesn't exists")

        cinema.city = city
        session.add(cinema)
        await session.commit()

        await session.refresh(cinema)

        return cinema.id

    def find_by_id(self) -> Base:
        return super().find_by_id()

    def update(self, obj_id: int, data: dict):
        return super().update(obj_id, data)

    def delete(self, obj_id: int) -> None:
        return super().delete(obj_id)
