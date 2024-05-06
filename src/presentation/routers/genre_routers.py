from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.presentation.dependency import Container
from src.service.category_service import GenreRepository

genre_router = APIRouter(tags=["category"])


@genre_router.get("/categories")
@inject
async def fetch_genres(
    service: GenreRepository = Depends(Provide[Container.genre_service]),
):
    return await service.find_all()


@genre_router.post("/categories")
@inject
async def fetch_categories(
    title: str,
    service: GenreRepository = Depends(Provide[Container.genre_service]),
):
    return await service.add_movie(title)
