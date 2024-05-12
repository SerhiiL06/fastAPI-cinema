from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from service.genre_service import GenreService
from src.presentation.dependency import Container

genre_router = APIRouter(tags=["category"])


@genre_router.get("/categories")
@inject
async def fetch_genres(
    session: AsyncSession,
    service: GenreService = Depends(Provide[Container.genre_service]),
):
    return await service.find_all(session)


@genre_router.post("/categories")
@inject
async def fetch_categories(
    session: AsyncSession,
    title: str,
    service: GenreService = Depends(Provide[Container.genre_service]),
):
    return await service.add_genre(title, session)
