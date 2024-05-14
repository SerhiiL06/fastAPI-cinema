from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.connections import session_transaction
from src.presentation.dependency import Container
from src.service.genre_service import GenreService

genre_router = APIRouter(tags=["category"])


@genre_router.get("/categories")
@inject
async def fetch_genres(
    session: Annotated[AsyncSession, Depends(session_transaction)],
    service: GenreService = Depends(Provide[Container.genre_service]),
):
    return await service.find_all(session)


@genre_router.post("/categories")
@inject
async def fetch_categories(
    session: Annotated[AsyncSession, Depends(session_transaction)],
    title: str,
    service: GenreService = Depends(Provide[Container.genre_service]),
):
    return await service.add_genre(title, session)
