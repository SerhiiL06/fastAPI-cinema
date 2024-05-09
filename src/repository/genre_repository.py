from typing import Union

from fastapi import HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.movie import Genre

from .abstract import AbstractRepository


class GenreRepository(AbstractRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session()

    async def find_all(self) -> list[Base]:
        q = select(Genre)

        result = await self.session.execute(q)

        return result.scalars().all()

    async def create(self, title: str) -> int:
        q = insert(Genre).values(title=title).returning(Genre.id)

        genre = await self.session.execute(q)
        await self.session.commit()
        return genre.scalar()

    async def find_by_id(self, entity_id: int) -> Base:
        return super().find_by_id(entity_id)

    async def find_by_title(
        self, title: Union[str, list], session: AsyncSession = None
    ):

        q = select(Genre)

        if type(title) in [list, tuple]:

            after_format = list(map(lambda x: x.capitalize(), title))
            q = q.where(Genre.title.in_(after_format))

        else:

            q = q.where(Genre.title == title.capitalize())

        result = await session.execute(q)

        if not result:
            raise HTTPException(404, "Genre with doesnt exists")

        return result.scalars().all()

    async def delete(self, entity_id: int) -> None:
        return super().delete(entity_id)

    async def update(self, entity_id: int, data: dict):
        return super().update(entity_id, data)
