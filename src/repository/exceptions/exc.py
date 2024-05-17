from src.infrastructure.database.models.base import Base


class DoesntExists(Exception):

    def __init__(self, model: Base) -> None:
        self.model = model.__name__
