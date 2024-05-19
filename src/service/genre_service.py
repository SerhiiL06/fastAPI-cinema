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

    async def fetch_by_id(self, genre_id: int, session: AsyncSession):

        genre = await self.repo.find_by_id(genre_id, session)

        return {"genre": genre}
