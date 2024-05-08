from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, UploadFile

from src.presentation.dependency import Container
from src.presentation.mappings.movie import CreateMovieDto
from src.service.impl.movie_service_impl import MovieServiceImpl

movies_router = APIRouter(tags=["movie"])


@movies_router.get("/movies")
@inject
async def get_movie_list(
    service: MovieServiceImpl = Depends(Provide[Container.movie_service]),
):
    return await service.fetch_all()


@movies_router.post("/movies")
@inject
async def create_movie(
    data: CreateMovieDto,
    # image: Annotated[bytes, UploadFile],
    service: MovieServiceImpl = Depends(Provide[Container.movie_service]),
):
    return await service.add_movie(data)
