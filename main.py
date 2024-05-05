from fastapi import FastAPI

from src.presentation.dependency import Container
from src.presentation.routers.cinema_routers import cinema_router


def application():

    app = FastAPI()
    app.include_router(cinema_router)

    container = Container()
    container.wire(packages=["src.presentation"])

    return app


app = application()
