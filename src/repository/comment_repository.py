from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.comments import Comment
from src.infrastructure.database.models.users import User
from src.repository.exceptions.exc import DoesntExists

from .abstract import AbstractRepository


class CommentRepository(AbstractRepository):

    async def create(self, data: dict, session: AsyncSession) -> int:
        q = insert(Comment).values(data).returning(Comment.id)

        res = await session.execute(q)

        await session.commit()

        return res.scalar()

    async def delete(self, entity_id: int, session: AsyncSession) -> None:
        comment = await session.get(Comment, entity_id)

        if comment is None:
            raise DoesntExists(Comment, entity_id)

        await session.delete(comment)
        await session.commit()

    async def find_all(self, movie_id: int, session: AsyncSession) -> list[Base]:
        q = (
            select(Comment)
            .where(Comment.movie_id == movie_id)
            .options(selectinload(Comment.author).load_only(User.nickname, User.id))
            .order_by(Comment.created_at.desc())
        )

        result = await session.execute(q)

        return result.scalars().all()

    async def find_comments_by_user(self, user_id: int, session: AsyncSession):
        q = select(Comment).where(Comment.author_id == user_id)

        result = await session.execute(q)

        return result.scalars().all()

    async def find_by_id(self, entity_id: int) -> Base:
        raise NotImplementedError()

    def update(self, entity_id: int, data: dict):
        raise NotImplementedError()
