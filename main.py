from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.presentation.dependency import Container
from src.presentation.routers.actor_routers import actor_routers
from src.presentation.routers.cinema_routers import cinema_router
from src.presentation.routers.genre_routers import genre_router
from src.presentation.routers.movie_routers import movies_router
from src.presentation.routers.user_routers import users_router
from src.repository.exceptions.exc import DoesntExists


def application():

    app = FastAPI()
    app.include_router(cinema_router)
    app.include_router(actor_routers)
    app.include_router(genre_router)
    app.include_router(movies_router)
    app.include_router(users_router)

    container = Container()
    container.config.db_name.from_env("DB_NAME")
    container.config.db_username.from_env("DB_USERNAME")
    container.config.db_password.from_env("DB_PASSWORD")
    container.config.db_host.from_env("DB_HOST")
    container.config.db_port.from_env("DB_PORT")
    container.wire(packages=["src.presentation"])

    return app


app = application()


@app.exception_handler(DoesntExists)
def doesnt_exists(request: Request, exc: DoesntExists):
    error_text = f"{exc.model} with value {exc.ident} doesnt exists"
    resp = JSONResponse(
        content={"code": "400", "msg": error_text},
        status_code=status.HTTP_404_NOT_FOUND,
    )
    return resp
