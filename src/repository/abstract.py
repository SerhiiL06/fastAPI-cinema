from abc import ABC, abstractmethod

from src.infrastructure.database.models.base import Base


class AbstractRepository(ABC):

    @abstractmethod
    def find_all(self) -> list[Base]:
        """Find list of entity"""

    @abstractmethod
    def find_by_id(self, entity_id: int) -> Base:
        """Retrieve entity by ident"""

    @abstractmethod
    def create(self, data: dict) -> int:
        """Create entity"""

    @abstractmethod
    def update(self, entity_id: int, data: dict):
        "Update entity"

    @abstractmethod
    def delete(self, entity_id: int) -> None:
        """Delete entity"""
