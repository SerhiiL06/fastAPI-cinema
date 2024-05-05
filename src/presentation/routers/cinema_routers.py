from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.infrastructure.database.connections import session_transaction
from src.presentation.mappings.cinema import CinemaDTO, CityDTO, UpdateCinemaDTO
from src.repository.cinema_repository import CinemaRepository
from src.service.cinema_service import CinemaService

from src.presentation.dependency import Container

cinema_router = APIRouter(tags=["cinema"])


@cinema_router.get("/cinemas")
@inject
async def fetch_cinemas(
    service: CinemaService = Depends(Provide[Container.service]),
):
    return await service.get_cinema_list()


@cinema_router.get("/cinemas/{cinema_id}")
@inject
async def detail_cinema(
    cinema_id: int,
    service: CinemaService = Depends(Provide[Container.service]),
):
    return await service.get_cinema(cinema_id)


@cinema_router.post("/city")
@inject
async def create_city(
    data: CityDTO,
    service: CinemaService = Depends(Provide[Container.service]),
):
    return await service.add_city(data)


@cinema_router.post("/cinemas", status_code=204)
@inject
async def create_cinema(
    data: CinemaDTO,
    service: CinemaService = Depends(Provide[Container.service]),
):
    return await service.add_cinema(data)


@cinema_router.delete("/cinemas/{cinema_id}/delete", status_code=204)
@inject
async def drop_cinema(
    cinema_id: int,
    session: Annotated[session_transaction, Depends()],
    service: CinemaService = Depends(Provide[Container.service]),
):
    return await service.destroy_cinema(cinema_id, session)


@cinema_router.patch("/cinemas/{cinema_id}/update")
@inject
async def update_cinema(
    cinema_id: int,
    data: UpdateCinemaDTO,
    service: CinemaService = Depends(Provide[Container.service]),
):
    return await service.update_cinema(cinema_id, data)