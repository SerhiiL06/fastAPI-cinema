from typing import Optional

from sqlalchemy import delete, extract, select, update
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.infrastructure.database.models.movie import Country, Genre, Movie, MovieGenre

from .abstract import AbstractRepository
from .actor_repository import ActorRepository
from .country_repository import CountryRepository
from .genre_repository import GenreRepository


class MovieRepository(CountryRepository, AbstractRepository):

    def __init__(self, actor_repo, genres_repo) -> None:
        self.actor_repo: ActorRepository = actor_repo
        self.genre_repo: GenreRepository = genres_repo

    async def find_all(self, page: int, session: AsyncSession) -> list[Movie]:

        offset = (page - 1) * 5
        q = (
            select(
                Movie.id,
                Movie.title,
                extract("YEAR", Movie.release_date).label("year"),
                Genre.title.label("genre"),
                Country.name.label("country"),
            )
            .join(Country, Movie.country_id == Country.id)
            .join(MovieGenre, Movie.id == MovieGenre.movie_id)
            .join(Genre, Genre.id == MovieGenre.genre_id)
            .where(Movie.is_publish)
            .order_by(Movie.created_at.desc())
            .offset(offset)
            .limit(5)
        )
        result: AsyncResult = await session.execute(q)

        return result.mappings().all()

    async def find_by_id(self, entity_id: int, session: AsyncSession) -> Movie:

        q = (
            select(Movie)
            .where(Movie.id == entity_id)
            .options(
                joinedload(Movie.country).load_only(Country.name),
                joinedload(Movie.genres),
                selectinload(Movie.actors),
            )
        )

        result = await session.execute(q)

        return result.scalars().one()

    async def find_by_slug(self, slug: str, session: AsyncSession) -> Optional[Movie]:

        q = (
            select(Movie)
            .where(Movie.slug == slug)
            .options(
                joinedload(Movie.country),
                joinedload(Movie.genres),
                joinedload(Movie.actors),
            )
        )

        result = await session.execute(q)

        return result.scalars().unique().one()

    async def create(self, data: dict, session) -> int:

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

        country = await self.country_by_title(country_name, session)
        genres = await self.genre_repo.find_by_title(genres, session)
        actors = await self.actor_repo.find_by_id(actors, session)

        new_movie.country = country

        for g in genres:
            new_movie.genres.append(g)

        for a in actors:
            new_movie.actors.append(a)

        session.add(new_movie)

        await session.commit()
        await session.refresh(new_movie)
        return new_movie.id

    async def update(self, entity_id: int, data: dict, session: AsyncSession) -> Movie:
        q = update(Movie).where(Movie.id == entity_id).values(data).returning(Movie)

        result = await session.execute(q)
        await session.execute()

        return result

    async def delete(self, entity_id: int, session: AsyncSession) -> None:
        q = delete(Movie).where(Movie.id == entity_id)

        await session.execute(q)
        await session.commit()
