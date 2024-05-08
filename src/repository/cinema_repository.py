from typing import Optional

from fastapi import HTTPException
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.infrastructure.database.models.cinema import Cinema, City

from .abstract import AbstractRepository


class CityRepository:

    async def get_city_by_id(self, city_id, session: AsyncSession) -> Optional[City]:

        return await session.get(City, city_id)

    async def create_city(self, data: dict) -> Optional[int]:

        query = insert(City).values(**data).returning(City.id)

        try:
            result = await self.session.execute(query)
            await self.session.commit()

            return result.scalar()
        except IntegrityError:
            raise HTTPException(400, "unique error")


class CinemaRepository(CityRepository, AbstractRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session = session()

    async def find_all(self) -> list[Cinema]:

        query = (
            select(Cinema)
            .options(joinedload(Cinema.city))
            .order_by(Cinema.title.asc(), Cinema.id.desc())
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, cinema: Cinema) -> int:
        city = await self.get_city_by_id(cinema.city_id, self.session)

        if city is None:
            raise HTTPException(404, "city with this id doesn't exists")

        cinema.city = city
        self.session.add(cinema)
        await self.session.commit()

        await self.session.refresh(cinema)

        return cinema.id

    async def find_by_id(self, entity_id: int) -> Cinema:

        cinema = await self.session.get(
            Cinema, entity_id, options=[joinedload(Cinema.city)]
        )

        if cinema is None:
            raise HTTPException(404, "cinema doesn't exists")

        return cinema

    async def update(self, entity_id: int, data: dict) -> None:
        query = (
            update(Cinema).where(Cinema.id == entity_id).values(**data).returning("*")
        )
        try:

            updated = await self.session.execute(query)
            await self.session.commit()
            return updated.mappings().all()
        except Exception:
            raise HTTPException(400, "Something went wrong!")

    async def delete(self, obj_id: int) -> None:
        query = await self.find_by_id(obj_id)

        await self.session.delete(query)
        await self.session.commit()
