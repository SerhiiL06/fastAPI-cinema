from dataclasses import asdict
from datetime import date, datetime
from typing import Optional, Union

from fastapi import HTTPException, UploadFile
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.movie import Movie
from src.presentation.mappings.movie import CreateMovieDto, UpdateMovieDto
from src.repository.comment_repository import CommentRepository
from src.repository.movie_repository import MovieRepository
from src.service.image_service import ImageService
from src.service.movie_service import MovieService


class MovieServiceImpl(MovieService):

    def __init__(self, repo: MovieRepository, image: ImageService) -> None:
        self.repo = repo
        self.image = image

    async def fetch_all(
        self,
        page: int,
        session: AsyncSession,
        text: Optional[str],
        year: Optional[int],
        genre: Optional[str],
    ) -> list[Movie]:
        return await self.repo.find_all(page, session, text, year, genre)

    async def add_movie(self, data: CreateMovieDto, image: UploadFile, session) -> int:

        self.validate_movie(data)

        dict_data = asdict(data)

        dict_data["image"] = self.image.save(image, dict_data.get("genres")[0])

        dict_data["slug"] = self.generate_slug(
            dict_data.get("title"),
            dict_data.get("country_id"),
            dict_data.get("release_date"),
        )

        movie_id = await self.repo.create(dict_data, session)

        return {"id": movie_id}

    async def fetch_by_slug(self, slug: str, session: AsyncSession) -> Optional[Movie]:

        movie = await self.repo.find_by_slug(slug, session)

        return {"movie": movie}

    async def fetch_by_id(
        self, entity_id: int, session: AsyncSession
    ) -> Optional[Movie]:
        movie = await self.repo.find_by_id(entity_id, session)

        return movie

    async def update_movie(
        self,
        entity_id: int,
        data: UpdateMovieDto,
        session: AsyncSession,
        image: UploadFile = None,
    ):
        self.validate_movie(data)

        movie_instance = await self.repo.find_by_id(entity_id, session)

        dict_data = self.clear_none(asdict(data))

        release_date = dict_data.get("release_date", movie_instance.release_date.year)
        genre = dict_data.get("genre", movie_instance.genres[0].title)
        image_path = movie_instance.image

        if dict_data.get("title"):
            dict_data["slug"] = self.generate_slug(
                dict_data.get("title"),
                movie_instance.id,
                release_date,
            )

        if image:
            dict_data["image"] = self.image.save(image, genre)

        update_instance = await self.repo.update(entity_id, dict_data, session)

        if image_path:
            self.image.delete(image_path)

        return {"after_update": update_instance}

    async def search(self, search_data: dict) -> list[Movie]:
        return super().search(search_data)

    @classmethod
    def generate_slug(self, title: str, movie_id: int, year: date) -> str:
        format_str = f"{movie_id}-{title}-{year}"
        slug = slugify(format_str)
        return slug

    @classmethod
    def validate_movie(cls, data: Union[CreateMovieDto, UpdateMovieDto]) -> None:

        errors = {}

        if data.release_date and data.release_date >= datetime.now().date():
            errors["date_error"] = "release date cannot be after current date"

        if data.duration and data.duration < 0:
            errors["duration_error"] = "duration must be a positiv integer"

        if data.description and len(data.description) < 5:
            errors["description_error"] = "description must be a five letter minimum"

        if errors:
            raise HTTPException(400, errors)

    @staticmethod
    def clear_none(data: dict) -> dict:

        clear_data = {}

        for k, v in data.items():
            if v:
                clear_data[k] = v

        return clear_data
