from dependency_injector import containers, providers

from src.infrastructure.database.connections import DatabaseCORE
from src.repository.actor_repository import ActorRepository
from src.repository.cinema_repository import CinemaRepository
from src.repository.genre_repository import GenreRepository
from src.repository.movie_repository import MovieRepository
from src.service.actor_service import ActorService
from src.service.category_service import GenreService
from src.service.cinema_service import CinemaService
from src.service.image_service import ImageService
from src.service.impl.movie_service_impl import MovieServiceImpl


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    db = providers.Singleton(
        DatabaseCORE,
        db_name=config.db_name,
        username=config.db_username,
        password=config.db_password,
        host=config.db_host,
        port=config.db_port,
    )

    image_service = providers.Factory(ImageService)
    cinema_repo = providers.Factory(CinemaRepository, db.provided.sesion_factory)
    cinema_service = providers.Factory(CinemaService, repo=cinema_repo)

    actor_repo = providers.Factory(ActorRepository, session=db.provided.session_factory)
    actor_service = providers.Factory(ActorService, repository=actor_repo)

    genre_repo = providers.Factory(GenreRepository, session=db.provided.session_factory)
    genre_service = providers.Factory(GenreService, repo=genre_repo)

    movie_repo = providers.Factory(MovieRepository, actor_repo, genre_repo)
    movie_service = providers.Factory(MovieServiceImpl, movie_repo, image_service)
