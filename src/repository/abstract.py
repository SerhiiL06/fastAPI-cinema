from abc import ABC, abstractmethod

from src.infrastructure.database.models.base import Base


class AbstractRepository(ABC):

    @abstractmethod
    def find_all(self) -> list[Base]:
        pass

    @abstractmethod
    def find_by_id(self) -> Base:
        pass

    @abstractmethod
    def create(self, data: dict) -> int:
        pass

    @abstractmethod
    def update(self, obj_id: int, data: dict):
        pass

    @abstractmethod
    def delete(self, obj_id: int) -> None:
        pass
