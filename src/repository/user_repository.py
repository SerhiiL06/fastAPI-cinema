from typing import Optional

from fastapi import HTTPException
from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.users import User

from .abstract import AbstractRepository


class UserRepository(AbstractRepository):

    async def create(self, data: dict, session: AsyncSession) -> int:
        q = insert(User).values(data).returning(User.id)
        try:
            user_id = await session.execute(q)
            await session.commit()

            return user_id
        except IntegrityError as e:
            raise HTTPException(400, f"user with this email already exists")

    async def find_by_id(self, entity_id: int, session: AsyncSession) -> Optional[User]:

        result = await session.get(User, entity_id)

        if result is None:
            raise HTTPException(404, "user doesn't exists")

        return result

    async def find_all(self, session: AsyncSession) -> list[User]:

        q = select(User)

        users = await session.execute(q)

        return users.scalars().all()

    async def update(self, entity_id: int, data: dict, session: AsyncSession) -> User:

        user_instance: User = await self.find_by_id(entity_id, session)

        user_instance.email = data.get("email", user_instance.email)
        user_instance.nickname = data.get("nickname", user_instance.nickname)

        await session.commit()
        await session.refresh(user_instance)

        return user_instance

    async def delete(self, entity_id: int, session: AsyncSession) -> None:
        instance = await self.find_by_id(entity_id)

        await session.delete(instance)
        await session.commit()
