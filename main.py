from fastapi import FastAPI

from src.presentation.dependency import Container
from src.presentation.routers.actor_routers import actor_routers
from src.presentation.routers.cinema_routers import cinema_router
from src.presentation.routers.genre_routers import genre_router


def application():

    app = FastAPI()
    app.include_router(cinema_router)
    app.include_router(actor_routers)
    app.include_router(genre_router)

    container = Container()
    container.config.db_name.from_env("DB_NAME")
    container.config.db_username.from_env("DB_USERNAME")
    container.config.db_password.from_env("DB_PASSWORD")
    container.config.db_host.from_env("DB_HOST")
    container.config.db_port.from_env("DB_PORT")
    container.wire(packages=["src.presentation"])

    return app


app = application()
