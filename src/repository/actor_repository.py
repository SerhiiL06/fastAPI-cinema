from fastapi import HTTPException
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.movie import Actor

from .abstract import AbstractRepository


class ActorRepository(AbstractRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session()

    async def find_all(self) -> list[Base]:
        async with self.session.begin() as connect:
            actors_list = await connect.execute(select(Actor))
            return actors_list.scalars().all()

    async def find_by_id(self, entity_id: int) -> Base:
        async with self.session.begin() as connect:
            result: AsyncResult = await connect.get(Actor, entity_id)

            if result is None:
                raise HTTPException(400, "object is not find")

            return result.scalars().all()

    async def create(self, data: dict) -> int:
        q = insert(Actor).values(**data).returning(Actor.id)

        try:
            async with self.session.begin() as connect:
                result = await connect.execute(q)
                await connect.commit()

                return result.scalar()
        except IntegrityError as e:
            raise HTTPException(400, "wrong country id")

    def update(self, entity_id: int, data: dict, sessiin: AsyncSession):
        return super().update(entity_id, data, sessiin)

    def delete(self, entity_id: int, session: AsyncSession) -> None:
        return super().delete(entity_id, session)
