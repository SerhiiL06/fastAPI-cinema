from typing import Optional

from fastapi import HTTPException
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession

from src.infrastructure.database.models.movie import Movie

from .abstract import AbstractRepository
from .actor_repository import ActorRepository
from .country_repository import CountryRepository
from .genre_repository import GenreRepository


class MovieRepository(CountryRepository, AbstractRepository):

    def __init__(self, session: AsyncSession, actor_repo, genres_repo) -> None:
        self.session: AsyncSession = session()
        self.actor_repo: ActorRepository = actor_repo
        self.genre_repo: GenreRepository = genres_repo

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

        country_name = data.pop("country_name")
        genres = data.pop("genres")
        actors = data.pop("actors")

        new_movie = Movie(
            title=data.get("title"),
            slug=data.get("slug"),
            description=data.get("description"),
            release_date=data.get("release_date"),
            duration=data.get("duration"),
        )

        async with self.session() as connect:
            country = await self.country_by_title(country_name, connect)
            genres = await self.genre_repo.find_by_title(genres)
            actors = await self.actor_repo.find_by_id(actors)

            new_movie.country = country

            for g in genres:
                new_movie.genres.append(g)

            for a in actors:
                new_movie.actors.append(a)

            connect.add(new_movie)

            await connect.commit()
            await connect.refresh(new_movie)
            return new_movie.id

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
