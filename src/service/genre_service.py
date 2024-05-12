from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.genre_repository import GenreRepository


class GenreService:

    def __init__(self, repo: GenreRepository) -> None:
        self.repo = repo

    async def fetch_all(self, session: AsyncSession):
        return await self.repo.find_all(session)

    async def add_genre(self, title: str, session: AsyncSession):
        category = await self.repo.create(title, session)

        return {"id": category}
