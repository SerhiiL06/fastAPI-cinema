from dependency_injector import containers, providers
from fastapi_mail import FastMail

from src.infrastructure.database.connections import DatabaseCORE
from src.infrastructure.database.redis import RedisCore
from src.infrastructure.settings import settings_factory
from src.repository.actor_repository import ActorRepository
from src.repository.cinema_repository import CinemaRepository
from src.repository.comment_repository import CommentRepository
from src.repository.genre_repository import GenreRepository
from src.repository.movie_repository import MovieRepository
from src.repository.tag_repository import TagRepository
from src.repository.user_repository import UserRepository
from src.service.actor_service import ActorService
from src.service.cinema_service import CinemaService
from src.service.genre_service import GenreService
from src.service.image_service import ImageService
from src.service.impl.auth_service import AuthService
from src.service.impl.comment_service_impl import CommentServiceImpl
from src.service.impl.email_service_impl import EmailServiceimpl
from src.service.impl.movie_service_impl import MovieServiceImpl
from src.service.impl.redis_service_impl import RedisServiceImpl
from src.service.impl.tag_service_impl import TagServiceImpl
from src.service.impl.token_service import TokenService
from src.service.impl.user_service_impl import UserServiceImpl
from src.service.password_service import PasswordService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    db = providers.Singleton(
        DatabaseCORE,
        db_name=config.postgres_db(),
        username=config.postgres_username(),
        password=config.postgres_password(),
        host=config.db_host(),
        port=config.db_port(),
    )

    redis = providers.Singleton(RedisCore, url="redis://redis")
    redis_service = providers.Factory(RedisServiceImpl, redis.provided.connection)

    email_core = providers.Singleton(FastMail, settings_factory.email_config)
    email_service = providers.Factory(EmailServiceimpl, email_core)

    image_service = providers.Factory(ImageService)

    cinema_repo = providers.Factory(CinemaRepository)
    cinema_service = providers.Factory(CinemaService, repo=cinema_repo)

    actor_repo = providers.Factory(ActorRepository)
    actor_service = providers.Factory(ActorService, repository=actor_repo)

    genre_repo = providers.Factory(GenreRepository)
    genre_service = providers.Factory(GenreService, repo=genre_repo)

    tag_repo = providers.Factory(TagRepository)
    tag_service = providers.Factory(TagServiceImpl, tag_repo)

    movie_repo = providers.Factory(MovieRepository, actor_repo, genre_repo, tag_repo)
    movie_service = providers.Factory(MovieServiceImpl, movie_repo, image_service)

    user_repo = providers.Factory(UserRepository)
    user_service = providers.Factory(UserServiceImpl, repo=user_repo)

    password_service = providers.Factory(PasswordService)
    token_service = providers.Factory(TokenService)
    auth_service = providers.Factory(
        AuthService, user_repo, password_service, token_service
    )

    comment_repo = providers.Factory(CommentRepository)

    comment_service = providers.Factory(CommentServiceImpl, comment_repo, movie_repo)


container = Container()


auth = container.auth_service()
