from dependency_injector import containers, providers

from src.infrastructure.database.connections import DatabaseCORE
from src.repository.cinema_repository import CinemaRepository
from src.service.cinema_service import CinemaService


class Container(containers.DeclarativeContainer):

    db = providers.Singleton(DatabaseCORE)
    repo = providers.Factory(CinemaRepository, session=db.provided.session)
    service = providers.Factory(CinemaService, repo=repo)
