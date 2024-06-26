from typing import Optional, Union

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.tag import Tag

from .abstract import AbstractRepository
from .exceptions.exc import AlreadyExists, DoesntExists


class TagRepository(AbstractRepository):

    async def find_all(self, session: AsyncSession) -> list[Tag]:
        q = select(Tag)

        tags = await session.execute(q)

        return tags.scalars().all()

    async def find_by_id(
        self, entity_id: Union[int, list[int]], session: AsyncSession
    ) -> Optional[Tag]:

        if isinstance(entity_id, list):
            return await self._find_by_list_values(entity_id, session)

        return await self._find_by_field(entity_id, session)

    async def find_by_title(self, entity_title: str, session: AsyncSession):
        return await self._find_by_field(entity_title, session)

    async def _find_by_field(self, field_info: Union[int, str], session: AsyncSession):
        q = select(Tag)

        if isinstance(field_info, str):
            q = q.where(Tag.title == field_info)

        else:
            q = q.where(Tag.id == field_info)

        tag = await session.execute(q)

        result = tag.scalars().one_or_none()

        if result is None:
            raise DoesntExists(Tag, field_info)

        return result

    async def _find_by_list_values(
        self, values: list[int], session: AsyncSession
    ) -> list[Tag]:

        q = select(Tag).where(Tag.id.in_(values))

        result = await session.execute(q)

        return result.scalars().all()

    async def create(self, data: Tag, session: AsyncSession) -> int:

        session.add(data)

        try:
            await session.commit()
            await session.refresh(data)
            return data

        except IntegrityError as _:
            raise AlreadyExists(Tag, data.title)

    async def update(self, entity_id: int, title: str, session: AsyncSession) -> Tag:

        tag = await self.find_by_id(entity_id, session)

        tag.title = title

        try:
            await session.commit()
            await session.refresh(tag)
            return tag

        except IntegrityError as _:
            raise AlreadyExists(Tag, title)

    async def delete(self, entity_id: int, session: AsyncSession) -> None:
        tag = await self.find_by_id(entity_id, session)

        await session.delete(tag)

        await session.commit()
