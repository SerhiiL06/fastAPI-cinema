from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.comment_repository import CommentRepository
from src.repository.movie_repository import MovieRepository
from src.service.comment_service import CommentService


class CommentServiceImpl(CommentService):
    def __init__(self, repo: CommentRepository, movie: MovieRepository) -> None:
        self.repo = repo
        self.movie_repo = movie

    async def add_comment(
        self, user_id: int, movie_id: int, comment_data: dict, session: AsyncSession
    ):
        movie = await self.movie_repo.find_by_id(movie_id, session)

        comment_data.update({"movie_id": movie.id, "author_id": user_id})

        comment_id = await self.repo.create(comment_data, session)

        return {"id": comment_id}

    async def delete_comment(self, comment_id: int, session: AsyncSession):
        await self.repo.delete(comment_id, session)

        return {"delete": "ok"}

    async def user_comments(self, user_id: int, session: AsyncSession):
        comments = await self.repo.find_comments_by_user(user_id, session)
        return {"user_comment": comments}
