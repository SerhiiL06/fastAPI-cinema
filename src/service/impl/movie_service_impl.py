from dataclasses import asdict
from datetime import date

from slugify import slugify

from src.infrastructure.database.models.movie import Movie
from src.presentation.mappings.movie import CreateMovieDto
from src.repository.movie_repository import MovieRepository
from src.service.movie_service import MovieService


class MovieServiceImpl(MovieService):

    def __init__(self, repo: MovieRepository) -> None:
        self.repo = repo

    async def fetch_all(self) -> list[Movie]:
        return await self.repo.find_all()

    async def add_movie(self, data: CreateMovieDto) -> int:
        dict_data = asdict(data)

        dict_data["slug"] = self.generate_slug(
            dict_data.get("title"),
            dict_data.get("country_id"),
            dict_data.get("release_date"),
        )
        await self.repo.create(dict_data)

    async def fetch_by_slug(self, slug: str) -> Movie | None:
        return super().fetch_by_slug(slug)

    async def fetch_by_id(self, entity_id: int) -> Movie | None:
        return await self.repo.find_by_id(entity_id)

    async def search(self, search_data: dict) -> list[Movie]:
        return super().search(search_data)

    @classmethod
    def generate_slug(self, title: str, movie_id: int, year: date) -> str:
        format_str = f"{movie_id}-{title}-{year}"
        slug = slugify(format_str)
        return slug
