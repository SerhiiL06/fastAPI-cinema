from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.base import Base


class AbstractRepository(ABC):

    @abstractmethod
    def find_all(self, session: AsyncSession) -> list[Base]:
        """Find list of entity"""

    @abstractmethod
    def find_by_id(self, entity_id: int, session: AsyncSession) -> Base:
        """Retrieve entity by ident"""

    @abstractmethod
    def create(self, data: dict) -> int:
        """Create entity"""

    @abstractmethod
    def update(self, entity_id: int, data: dict, sessiin: AsyncSession):
        "Update entity"

    @abstractmethod
    def delete(self, entity_id: int, session: AsyncSession) -> None:
        """Delete entity"""
