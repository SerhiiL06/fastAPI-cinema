from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.common.factories import current_user, session_factory
from src.common.permissions import check_role
from src.presentation.dependency import Container
from src.service.genre_service import GenreService

genre_router = APIRouter(tags=["category"])


@genre_router.get("/genres")
@check_role(["regular"])
@inject
async def fetch_genres(
    session: session_factory,
    user: current_user,
    service: GenreService = Depends(Provide[Container.genre_service]),
):
    return await service.fetch_all(session)


@genre_router.get("/genres/{genre_id}")
@check_role(["regular"])
@inject
async def fetch_genres(
    genre_id: int,
    user: current_user,
    session: session_factory,
    service: GenreService = Depends(Provide[Container.genre_service]),
):
    return await service.fetch_by_id(genre_id, session)


@genre_router.post("/genres")
@check_role(["regular"])
@inject
async def fetch_categories(
    session: session_factory,
    title: str,
    service: GenreService = Depends(Provide[Container.genre_service]),
):
    return await service.add_genre(title, session)
