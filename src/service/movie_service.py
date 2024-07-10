from abc import ABC, abstractmethod
from typing import Optional

from src.infrastructure.database.models.movie import Movie


class MovieService(ABC):

    @abstractmethod
    def fetch_all(self) -> list[Movie]:
        pass

    @abstractmethod
    def fetch_by_slug(self, slug: str) -> Optional[Movie]:
        pass

    @abstractmethod
    def fetch_by_id(self, entity_id: int) -> Optional[Movie]:
        pass

    @abstractmethod
    def search(self, search_data: dict) -> list[Movie]:
        pass

    @abstractmethod
    def add_movie(self, data: dict) -> int:
        pass

    @abstractmethod
    def rating_movie(self, entity_id: int, user_id: int, rating: int) -> dict:
        pass
