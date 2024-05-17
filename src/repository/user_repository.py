from typing import Optional, Union

from fastapi import HTTPException
from sqlalchemy import Date, cast, delete, insert, or_, select
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

            return user_id.scalar()
        except IntegrityError as e:
            raise HTTPException(400, f"user with this email already exists")

    async def find_by_id(self, entity_id: int, session: AsyncSession) -> Optional[User]:
        return await self._find_by_field(entity_id, session)

    async def find_by_email(self, email: str, session: AsyncSession):
        return await self._find_by_field(email, session)

    async def find_by_nickname(
        self, nickname: str, session: AsyncSession
    ) -> Optional[User]:
        return await self._find_by_field(nickname, session)

    async def _find_by_field(
        self, search_field: Union[str, int], session: AsyncSession
    ):
        q = select(User)

        if isinstance(search_field, str):
            q = q.where(or_(User.email == search_field, User.nickname == search_field))
        else:
            q = q.where(User.id == search_field)

        result = await session.execute(q)

        to_return = result.scalars().one_or_none()

        if to_return is None:
            raise HTTPException(404, "user doesnt exists")

        return to_return

    async def find_all(self, session: AsyncSession) -> list[User]:

        q = select(
            User.id,
            User.email,
            User.nickname,
            cast(User.joined_at, Date),
            User.is_active,
            User.verificate,
            User.role,
        )

        users = await session.execute(q)

        return users.mappings().all()

    async def update(self, entity_id: int, data: dict, session: AsyncSession) -> User:

        user_instance: User = await self.find_by_id(entity_id, session)

        user_instance.email = data.get("email", user_instance.email)
        user_instance.nickname = data.get("nickname", user_instance.nickname)
        user_instance.is_active = data.get("is_active", user_instance.is_active)
        user_instance.verificate = data.get("verificate", user_instance.verificate)

        await session.commit()
        await session.refresh(user_instance)

        return user_instance

    async def delete(self, entity_id: int, session: AsyncSession) -> None:
        instance = await self.find_by_id(entity_id)

        await session.delete(instance)
        await session.commit()
