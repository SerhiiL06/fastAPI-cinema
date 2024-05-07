from src.infrastructure.database.models.movie import Movie
from src.repository.movie_repository import MovieRepository
from src.service.movie_service import MovieService


class MovieServiceImpl(MovieService):

    def __init__(self, repo: MovieRepository) -> None:
        self.repo = repo

    async def fetch_all(self) -> list[Movie]:
        return await self.repo.find_all()

    async def fetch_by_slug(self, slug: str) -> Movie | None:
        return super().fetch_by_slug(slug)

    async def fetch_by_id(self, entity_id: int) -> Movie | None:
        return await self.repo.find_by_id(entity_id)

    async def search(self, search_data: dict) -> list[Movie]:
        return super().search(search_data)
