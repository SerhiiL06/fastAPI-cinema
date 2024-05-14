from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.connections import session_transaction
from src.presentation.dependency import Container
from src.presentation.mappings.cinema import (CinemaDTO, CityDTO,
                                              UpdateCinemaDTO)
from src.service.cinema_service import CinemaService

cinema_router = APIRouter(tags=["cinema"])


@cinema_router.get("/cinemas")
@inject
async def fetch_cinemas(
    session: Annotated[AsyncSession, Depends(session_transaction)],
    service: CinemaService = Depends(Provide[Container.cinema_service]),
):
    return await service.get_cinema_list(session)


@cinema_router.get("/cinemas/{cinema_id}")
@inject
async def detail_cinema(
    session: Annotated[AsyncSession, Depends(session_transaction)],
    cinema_id: int,
    service: CinemaService = Depends(Provide[Container.cinema_service]),
):
    return await service.get_cinema(cinema_id, session)


@cinema_router.post("/city")
@inject
async def create_city(
    session: Annotated[AsyncSession, Depends(session_transaction)],
    data: CityDTO,
    service: CinemaService = Depends(Provide[Container.cinema_service]),
):
    return await service.add_city(data, session)


@cinema_router.post("/cinemas", status_code=204)
@inject
async def create_cinema(
    session: Annotated[AsyncSession, Depends(session_transaction)],
    data: CinemaDTO,
    service: CinemaService = Depends(Provide[Container.cinema_service]),
):
    return await service.add_cinema(data, session)


@cinema_router.delete("/cinemas/{cinema_id}/delete", status_code=204)
@inject
async def drop_cinema(
    session: Annotated[AsyncSession, Depends(session_transaction)],
    cinema_id: int,
    service: CinemaService = Depends(Provide[Container.cinema_service]),
):
    return await service.destroy_cinema(cinema_id, session)


@cinema_router.patch("/cinemas/{cinema_id}/update")
@inject
async def update_cinema(
    session: Annotated[AsyncSession, Depends(session_transaction)],
    cinema_id: int,
    data: UpdateCinemaDTO,
    service: CinemaService = Depends(Provide[Container.cinema_service]),
):
    return await service.update_cinema(cinema_id, data, session)
