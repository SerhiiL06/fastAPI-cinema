from typing import Optional, Union

from sqlalchemy import delete, extract, select
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession
from sqlalchemy.orm import joinedload

from src.infrastructure.database.models.movie import (Country, Genre, Movie,
                                                      MovieGenre)

from .abstract import AbstractRepository
from .actor_repository import ActorRepository
from .country_repository import CountryRepository
from .exceptions.exc import DoesntExists
from .genre_repository import GenreRepository


class MovieRepository(CountryRepository, AbstractRepository):

    def __init__(self, actor_repo, genres_repo) -> None:
        self.actor_repo: ActorRepository = actor_repo
        self.genre_repo: GenreRepository = genres_repo

    async def find_all(
        self,
        page: int,
        session: AsyncSession,
        text: Optional[None],
        year: Optional[int],
        genre: Optional[str],
    ) -> list[Movie]:

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

        if text:
            q = q.where(Movie.title.icontains(text))

        if year:
            q = q.where(extract("YEAR", Movie.release_date) == year)

        if genre:
            q = q.where(Genre.title.icontains(genre))

        result: AsyncResult = await session.execute(q)

        return result.mappings().all()

    async def find_by_id(
        self, entity_id: int, session: AsyncSession
    ) -> Optional[Movie]:
        return await self._find_by_slug_or_id(entity_id, session)

    async def find_by_slug(self, slug: str, session: AsyncSession) -> Optional[Movie]:
        return await self._find_by_slug_or_id(slug, session)

    async def _find_by_slug_or_id(
        self,
        search_arg: Union[str, int],
        session: AsyncSession,
    ) -> Optional[Movie]:

        q = select(Movie).options(
            joinedload(Movie.country).load_only(Country.name),
            joinedload(Movie.genres),
            joinedload(Movie.actors),
        )

        if isinstance(search_arg, int):
            q = q.where(Movie.id == search_arg)
        else:
            q = q.where(Movie.slug == search_arg)

        result = await session.execute(q)

        instance = result.scalars().unique().one_or_none()

        if instance is None:
            raise DoesntExists(model=Movie)

        return instance

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

        new_movie = self.connect_relations(new_movie, genres, actors)

        session.add(new_movie)

        await session.commit()
        await session.refresh(new_movie)
        return new_movie.id

    async def update(self, entity_id: int, data: dict, session: AsyncSession) -> Movie:

        genres = await self.genre_repo.find_by_title(data.pop("genres", ()), session)
        actors = await self.actor_repo.find_by_id(data.pop("actors", ()), session)

        instance = await session.get(Movie, entity_id)

        instance = self.connect_relations(instance, genres, actors)

        instance.title = data.get("title", instance.title)
        instance.description = data.get("description", instance.description)
        instance.release_date = data.get("release_date", instance.release_date)
        instance.country_id = data.get("country_id", instance.country_id)
        instance.image = data.get("image", instance.image)
        instance.duration = data.get("diration", instance.duration)

        await session.commit()

        await session.refresh(instance)

        return {"after_update": instance}

    async def delete(self, entity_id: int, session: AsyncSession) -> None:
        q = delete(Movie).where(Movie.id == entity_id)

        await session.execute(q)
        await session.commit()

    @classmethod
    def connect_relations(
        cls, instance: Movie, genres: Union[list, None], actors: Union[list, None]
    ) -> Movie:

        if genres:
            for g in genres:
                instance.genres.append(g)

        if actors is not None:
            for a in actors:
                instance.actors.append(a)

        return instance
