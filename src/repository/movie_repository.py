from typing import Optional

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.movie import Movie

from .abstract import AbstractRepository


class MovieRepository(AbstractRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session()

    async def find_all(self) -> list[Movie]:

        q = select(Movie).where(Movie.is_publish)
        async with self.session() as connect:
            result: AsyncResult = await connect.execute(q)

            return result.scalars().all()

    async def find_by_id(self, entity_id: int) -> Movie:

        q = select(Movie).where(Movie.id == entity_id)

        async with self.session() as connect:
            result: AsyncResult = await connect.execute(q)

            return result.scalars().one()

    async def find_by_slug(self, slug: str) -> Optional[Movie]:
        q = select(Movie).where(Movie.slug == slug)

        async with self.session() as connect:
            result = await connect.execute(q)

            return result.scalars().one()

    async def create(self, data: dict) -> int:

        q = insert(Movie).values(data).returning(Movie.id)

        async with self.session() as connect:
            result = await connect.execute(q)
            await connect.commit()

            return result.slalar()

    async def update(self, entity_id: int, data: dict) -> Movie:
        q = update(Movie).where(Movie.id == entity_id).values(data).returning(Movie)

        async with self.session() as connect:
            result = await connect.execute(q)
            await connect.execute()

            return result

    async def delete(self, entity_id: int) -> None:
        q = delete(Movie).where(Movie.id == entity_id)

        async with self.session() as connect:
            await connect.execute(q)
            await connect.commit()
