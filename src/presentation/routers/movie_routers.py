from datetime import date
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, File, Form, UploadFile

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
    image: UploadFile = File(),
    title: str = Body(),
    description: str = Body(),
    release_date: date = Body(),
    duration: int = Body(),
    country_name: str = Body(),
    genres: list[str] = Body(),
    actors: list[int] = Body(),
    service: MovieServiceImpl = Depends(Provide[Container.movie_service]),
):
    dto = CreateMovieDto(
        title,
        description,
        release_date,
        duration,
        country_name,
        genres,
        actors,
    )
    return await service.add_movie(dto, image)
