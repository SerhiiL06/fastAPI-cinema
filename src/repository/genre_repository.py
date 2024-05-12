from typing import Optional, Union

from fastapi import HTTPException
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.movie import Genre

from .abstract import AbstractRepository


class GenreRepository(AbstractRepository):

    async def find_all(self, session: AsyncSession) -> list[Base]:
        q = select(Genre)

        result = await session.execute(q)

        return result.scalars().all()

    async def create(self, title: str, session: AsyncSession) -> int:
        q = insert(Genre).values(title=title).returning(Genre.id)

        genre = await session.execute(q)
        await session.commit()
        return genre.scalar()

    async def find_by_id(
        self, entity_id: int, session: AsyncSession
    ) -> Optional[Genre]:
        genre = await session.get(Genre, entity_id)

        if genre is None:
            raise HTTPException(400, f"genre with {id} doesnt exists")

        return genre

    async def find_by_title(self, title: Union[str, list], session: AsyncSession):

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

    async def delete(self, entity_id: int, session: AsyncSession) -> None:
        q = delete(Genre).where(Genre.id == entity_id)

        await session.execute(q)

        await session.commit()

    async def update(self, entity_id: int, data: dict, session: AsyncSession) -> Genre:

        genre_instance = await self.find_by_id(entity_id, session)

        genre_instance.title = data.get("title", genre_instance.title)

        await session.commit()

        await session.refresh(genre_instance)

        return genre_instance
