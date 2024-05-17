from datetime import date
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, File, Query, UploadFile

from src.common.factories import current_user, session_factory
from src.presentation.dependency import Container
from src.presentation.mappings.movie import CreateMovieDto, UpdateMovieDto
from src.service.impl.movie_service_impl import MovieServiceImpl

movies_router = APIRouter(tags=["movie"])


@movies_router.get("/movies")
@inject
async def get_movie_list(
    session: session_factory,
    service: MovieServiceImpl = Depends(Provide[Container.movie_service]),
    page: int = Query(1, gt=0),
    text: str = Query(None),
    year: int = Query(None),
    genre: str = Query(None),
):

    return await service.fetch_all(page, session, text, year, genre)


@movies_router.post("/movies")
@inject
async def create_movie(
    session: session_factory,
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
        genres[0].split(","),
        actors,
    )
    return await service.add_movie(dto, image, session)


@movies_router.get("/movies/{movie_id}")
@inject
async def retrive_movie_by_id(
    movie_id: int,
    session: session_factory,
    service: MovieServiceImpl = Depends(Provide[Container.movie_service]),
):
    return await service.fetch_by_id(movie_id, session)


@movies_router.get("/movies/find-by-slug/{movie_slug}")
@inject
async def retrive_movie_by_slug(
    movie_slug: str,
    session: session_factory,
    service: MovieServiceImpl = Depends(Provide[Container.movie_service]),
):
    return await service.fetch_by_slug(movie_slug, session)


@movies_router.patch("/movies/{movie_id}")
@inject
async def update_movie(
    movie_id: int,
    session: session_factory,
    image: UploadFile = File(None),
    title: str = Body(None),
    description: str = Body(None),
    release_date: date = Body(None),
    duration: int = Body(None),
    country_name: str = Body(None),
    genres: list[str] = Body(None),
    actors: list[int] = Body(None),
    service: MovieServiceImpl = Depends(Provide[Container.movie_service]),
):
    genres = genres[0].split(",") if genres else None
    data = UpdateMovieDto(
        title,
        description,
        release_date,
        duration,
        country_name,
        genres,
        actors,
    )

    return await service.update_movie(movie_id, data, session, image)
