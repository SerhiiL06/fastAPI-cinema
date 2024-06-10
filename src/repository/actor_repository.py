from typing import Optional, Union

from fastapi import HTTPException
from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.infrastructure.database.models.movie import Actor, Country

from .abstract import AbstractRepository


class ActorRepository(AbstractRepository):

    async def find_all(self, session: AsyncSession) -> list[Actor]:

        actors_list = await session.execute(
            select(Actor).options(joinedload(Actor.country).load_only(Country.name))
        )
        return actors_list.scalars().all()

    async def find_by_id(
        self, entity_id: Union[int, list[int]], session: AsyncSession
    ) -> Optional[Union[Actor, list[Actor]]]:

        q = select(Actor)

        if type(entity_id) in [list, tuple]:
            q = q.where(Actor.id.in_(entity_id))
        else:
            q = q.where(Actor.id == entity_id)

        result = await session.execute(q)

        return result.scalars().all()

    async def create(self, actor: Actor, session: AsyncSession) -> int:
        try:
            session.add(actor)
            await session.commit()

            await session.refresh(actor)

            return actor
        except IntegrityError as e:
            raise HTTPException(400, "wrong country id")

    def update(self, entity_id: int, data: dict, session):
        return super().update(entity_id, data)

    async def delete(self, entity_id: int, session) -> None:
        q = delete(Actor).where(Actor.id == entity_id)

        await session.execute(q)
        await session.commit()
