from dataclasses import asdict
from datetime import date, datetime
from typing import Optional

from fastapi import HTTPException, UploadFile
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.movie import Movie
from src.presentation.mappings.movie import CreateMovieDto
from src.repository.movie_repository import MovieRepository
from src.service.image_service import ImageService
from src.service.movie_service import MovieService
from sqlalchemy.ext.asyncio import AsyncSession


class MovieServiceImpl(MovieService):

    def __init__(self, repo: MovieRepository, image: ImageService) -> None:
        self.repo = repo
        self.image = image

    async def fetch_all(
        self,
        page: int,
        session: AsyncSession,
    ) -> list[Movie]:
        return await self.repo.find_all(page, session)

    async def add_movie(self, data: CreateMovieDto, image: UploadFile, session) -> int:

        self.validate_movie(data)

        dict_data = asdict(data)

        dict_data["image"] = self.image.save(image, dict_data.get("genres"))

        dict_data["slug"] = self.generate_slug(
            dict_data.get("title"),
            dict_data.get("country_id"),
            dict_data.get("release_date"),
        )
        movie_id = await self.repo.create(dict_data, session)
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

    async def search(self, search_data: dict) -> list[Movie]:
        return super().search(search_data)

    @classmethod
    def generate_slug(self, title: str, movie_id: int, year: date) -> str:
        format_str = f"{movie_id}-{title}-{year}"
        slug = slugify(format_str)
        return slug

    @classmethod
    def validate_movie(cls, data: CreateMovieDto) -> None:

        errors = {}

        if data.release_date >= datetime.now().date():
            errors["date_error"] = "release date cannot be after current date"

        if data.duration < 0:
            errors["duration_error"] = "duration must be a positiv integer"

        if len(data.description) < 5:
            errors["description_error"] = "description must be a five letter minimum"

        if errors:
            raise HTTPException(400, errors)
