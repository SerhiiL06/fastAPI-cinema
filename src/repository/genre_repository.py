from typing import Union

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.movie import Genre

from .abstract import AbstractRepository


class GenreRepository(AbstractRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session()

    async def find_all(self) -> list[Base]:
        async with self.session() as connect:
            q = select(Genre)

            result = await connect.execute(q)

            return result.scalars().all()

    async def create(self, title: str) -> int:
        q = insert(Genre).values(title=title).returning(Genre.id)

        async with self.session() as connect:
            genre = await connect.execute(q)
            await connect.commit()
            return genre.scalar()

    async def find_by_id(self, entity_id: int) -> Base:
        return super().find_by_id(entity_id)

    async def find_by_title(self, title: Union[str, list]):
        q = select(Genre)
        if isinstance(title, list):
            q = q.where(Genre.title.in_(title))
        else:
            q = q.where(Genre.title == title)

        async with self.session() as connect:
            result = await connect.execute(q)
            return result.scalars().all()

    async def delete(self, entity_id: int) -> None:
        return super().delete(entity_id)

    async def update(self, entity_id: int, data: dict):
        return super().update(entity_id, data)
