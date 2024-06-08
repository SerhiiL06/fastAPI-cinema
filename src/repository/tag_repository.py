from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.models.base import Base
from src.infrastructure.database.models.tag import Tag

from .abstract import AbstractRepository
from .exceptions.exc import DoesntExists


class TagRepository(AbstractRepository):

    async def find_all(self, session: AsyncSession) -> list[Tag]:
        q = select(Tag)

        tags = await session.execute(q)

        return tags.scalars().all()

    async def find_by_id(self, entity_id: int, session: AsyncSession) -> Optional[Tag]:
        q = select(Tag).where(Tag.id == entity_id)

        tag = await session.execute(q)

        result = tag.one_or_none()

        if result is None:
            raise DoesntExists(Tag, entity_id)

        return result

    async def create(self, data: Tag, session: AsyncSession) -> int:

        session.add(data)

        await session.commit()

        await session.refresh(data)

        return data

    async def update(self, entity_id: int, title: str, session: AsyncSession) -> Tag:

        tag = await self.find_by_id(entity_id, session)

        tag.title = title

        await session.commit()

        await session.refresh(tag)

        return tag

    async def delete(self, entity_id: int, session: AsyncSession) -> None:
        tag = await self.find_by_id(entity_id)

        session.delete(tag)

        await session.commit()
