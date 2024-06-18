from dataclasses import asdict
from datetime import date

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, File, Query, UploadFile

from src.common.factories import current_user, session_factory
from src.common.permissions import check_role
from src.common.utils import order_types
from src.presentation.dependency import Container
from src.presentation.mappings.comment import CreateCommentDto
from src.presentation.mappings.movie import CreateMovieDto, UpdateMovieDto
from src.service.impl.comment_service_impl import CommentServiceImpl
from src.service.impl.movie_service_impl import MovieServiceImpl
from src.service.impl.redis_service_impl import RedisServiceImpl

movies_router = APIRouter(tags=["movie"])


@movies_router.get("/movies")
@inject
async def movie_list(
    session: session_factory,
    service: MovieServiceImpl = Depends(Provide[Container.movie_service]),
    page: int = Query(1, gt=0),
    text: str = Query(None),
    year: int = Query(None),
    genre: str = Query(None),
    ordering: str = Query("new", regex=order_types),
):

    return await service.fetch_all(session, text, year, genre, ordering, page)


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
    tags: list[int] = Body(),
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
        tags,
    )
    return await service.add_movie(dto, image, session)


@movies_router.get("/movies/{movie_slug}")
@inject
async def retrive_movie_by_slug(
    movie_slug: str,
    session: session_factory,
    cache_service: RedisServiceImpl = Depends(Provide[Container.redis_service]),
    service: MovieServiceImpl = Depends(Provide[Container.movie_service]),
):
    return await service.fetch_by_slug(movie_slug, cache_service, session)


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


@movies_router.get("/movies/genre/{genre_slug}")
@inject
async def fetch_by_genre(
    session: session_factory,
    genre_slug: str,
    page: int = Query(1, gt=0),
    service: MovieServiceImpl = Depends(Provide[Container.movie_service]),
):
    return await service.fetch_all(genre=genre_slug, page=page, session=session)


@movies_router.post("/movies/{movie_id}/comment")
@inject
async def comment_movie(
    user: current_user,
    movie_id: int,
    comment: CreateCommentDto,
    session: session_factory,
    service: CommentServiceImpl = Depends(Provide[Container.comment_service]),
):
    return await service.add_comment(
        user.get("user_id"), movie_id, asdict(comment), session
    )


@movies_router.delete("/movies/{comment_id}/delete")
@check_role(["regular"])
@inject
async def drop_comment(
    user: current_user,
    comment_id: int,
    session: session_factory,
    service: CommentServiceImpl = Depends(Provide[Container.comment_service]),
):
    return await service.delete_comment(comment_id, session)
