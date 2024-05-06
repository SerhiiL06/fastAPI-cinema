from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.movie import Actor

from .abstract import AbstractRepository


class ActorRepository(AbstractRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_all(self) -> list[Base]:
        async with self.session() as connect:
            actors_list = await connect.execute(select(Actor))
            return actors_list.scalars().all()

    async def find_by_id(self, entity_id: int, session: AsyncSession) -> Base:
        return super().find_by_id(entity_id, session)

    def create(self, data: dict) -> int:
        return super().create(data)

    def update(self, entity_id: int, data: dict, sessiin: AsyncSession):
        return super().update(entity_id, data, sessiin)

    def delete(self, entity_id: int, session: AsyncSession) -> None:
        return super().delete(entity_id, session)
