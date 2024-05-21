from src.infrastructure.database.models.base import Base


class DoesntExists(Exception):

    def __init__(self, model: Base, ident: int) -> None:
        self.model = model.__name__
        self.ident = ident
