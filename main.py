from fastapi import FastAPI

from src.presentation.dependency import Container
from src.presentation.exceptions.exc import PermissionDanied, permission_danied
from src.presentation.routers.actor_routers import actor_routers
from src.presentation.routers.auth_routers import auth_routers
from src.presentation.routers.cinema_routers import cinema_router
from src.presentation.routers.genre_routers import genre_router
from src.presentation.routers.movie_routers import movies_router
from src.presentation.routers.tag_routers import tag_router
from src.presentation.routers.user_routers import users_router
from src.repository.exceptions.exc import (AlreadyExists, DoesntExists,
                                           already_exists, doesnt_exists)
from src.service.exceptions.exc import ValidationError, validation_error
from src.service.middlewares.rate_limits import rate_limit_lifespan


def application():

    app = FastAPI(lifespan=rate_limit_lifespan)

    app.include_router(actor_routers)
    app.include_router(auth_routers)
    app.include_router(cinema_router)
    app.include_router(genre_router)
    app.include_router(movies_router)
    app.include_router(users_router)
    app.include_router(tag_router)

    app.add_exception_handler(DoesntExists, doesnt_exists)
    app.add_exception_handler(AlreadyExists, already_exists)
    app.add_exception_handler(PermissionDanied, permission_danied)
    app.add_exception_handler(ValidationError, validation_error)

    container = Container()
    container.config.db_name.from_env("POSTGRES_DB")
    container.config.db_username.from_env("POSTGRES_USERNAME")
    container.config.db_password.from_env("POSTGRES_PASSWORD")
    container.config.db_host.from_env("DB_HOST")
    container.config.db_port.from_env("DB_PORT")
    container.config.redis_url.from_env("REDIS_URL")
    container.wire(packages=["src.presentation", "src.service.middlewares"])

    return app


app = application()
