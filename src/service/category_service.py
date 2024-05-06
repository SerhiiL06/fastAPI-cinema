from src.repository.genre_repository import GenreRepository


class GenreService:

    def __init__(self, repo: GenreRepository) -> None:
        self.repo = repo

    async def fetch_all(self):
        return await self.repo.find_all()

    async def add_movie(self, title: str):
        category = await self.repo.create(title)

        return {"id": category}
