from fastapi import HTTPException
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession
from sqlalchemy.orm import joinedload

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.movie import Actor, Country

from .abstract import AbstractRepository


class ActorRepository(AbstractRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session()

    async def find_all(self) -> list[Base]:
        async with self.session() as connect:
            actors_list = await connect.execute(
                select(Actor).options(joinedload(Actor.country).load_only(Country.name))
            )
            return actors_list.scalars().all()

    async def find_by_id(self, entity_id: int) -> Base:
        async with self.session() as connect:
            result: AsyncResult = await connect.get(Actor, entity_id)

            if result is None:
                raise HTTPException(400, "object is not find")

            return result.scalars().all()

    async def create(self, data: dict) -> int:
        q = insert(Actor).values(**data).returning(Actor.id)

        try:
            async with self.session as connect:
                result = await connect.execute(q)
                await connect.commit()

                return result.scalar()
        except IntegrityError as e:
            raise HTTPException(400, "wrong country id")

    def update(self, entity_id: int, data: dict):
        return super().update(entity_id, data)

    async def delete(self, entity_id: int) -> None:
        q = delete(Actor).where(Actor.id == entity_id)
        async with self.session() as connect:
            await connect.execute(q)
            await connect.commit()
