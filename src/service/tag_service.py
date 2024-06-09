from abc import ABC, abstractmethod
from typing import Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.tag import Tag


class TagService(ABC):

    @abstractmethod
    def create_tag(self, title: str, session: AsyncSession) -> int:
        raise NotImplementedError()

    @abstractmethod
    def fetch_tags(self, session: AsyncSession) -> list[Tag]:
        raise NotImplementedError()

    @abstractmethod
    def fetch_tag_info(
        self, tag_info: Union[str, int], session: AsyncSession
    ) -> Optional[Tag]:
        raise NotImplementedError()

    @abstractmethod
    def update_tag(self, tag_id: int, title: str, session: AsyncSession) -> Tag:
        raise NotImplementedError()

    @abstractmethod
    def drop_tag(self, tag_id: int, session: AsyncSession) -> None:
        raise NotImplementedError()
