from dependency_injector import containers, providers

from src.infrastructure.database.connections import DatabaseCORE
from src.repository.actor_repository import ActorRepository
from src.repository.cinema_repository import CinemaRepository
from src.service.actor_service import ActorService
from src.service.cinema_service import CinemaService


class Container(containers.DeclarativeContainer):

    db = providers.Singleton(DatabaseCORE)

    cinema_repo = providers.Factory(
        CinemaRepository, session=db.provided.session_transaction
    )
    cinema_service = providers.Factory(CinemaService, repo=cinema_repo)

    actor_repo = providers.Factory(
        ActorRepository, session=db.provided.session_transaction
    )
    actor_service = providers.Factory(ActorService, repository=actor_repo)
