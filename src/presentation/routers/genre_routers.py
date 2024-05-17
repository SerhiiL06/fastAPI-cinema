from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.factories import current_user, session_factory
from src.presentation.dependency import Container
from src.service.genre_service import GenreService

genre_router = APIRouter(tags=["category"])


@genre_router.get("/categories")
@inject
async def fetch_genres(
    session: session_factory,
    service: GenreService = Depends(Provide[Container.genre_service]),
):
    return await service.find_all(session)


@genre_router.post("/categories")
@inject
async def fetch_categories(
    session: session_factory,
    title: str,
    service: GenreService = Depends(Provide[Container.genre_service]),
):
    return await service.add_genre(title, session)
