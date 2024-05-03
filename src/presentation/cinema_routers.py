from typing import Annotated

from fastapi import APIRouter, Depends

from src.infrastructure.database.connections import session_transaction
from src.presentation.mappings.cinema import (CinemaDTO, CityDTO,
                                              UpdateCinemaDTO)
from src.service.cinema_service import CinemaService

cinema_router = APIRouter(tags=["cinema"])


@cinema_router.get("/cinemas")
async def fetch_cinemas(
    service: Annotated[CinemaService, Depends()],
    session: Annotated[session_transaction, Depends()],
):
    return await service.get_cinema_list(session)


@cinema_router.get("/cinemas/{cinema_id}")
async def detail_cinema(
    cinema_id: int,
    service: Annotated[CinemaService, Depends()],
    session: Annotated[session_transaction, Depends()],
):
    return await service.get_cinema(cinema_id, session)


@cinema_router.post("/city")
async def create_city(
    data: CityDTO,
    service: Annotated[CinemaService, Depends()],
    session: Annotated[session_transaction, Depends()],
):
    return await service.add_city(data, session)


@cinema_router.post("/cinemas", status_code=204)
async def create_cinema(
    data: CinemaDTO,
    service: Annotated[CinemaService, Depends()],
    session: Annotated[session_transaction, Depends()],
):
    return await service.add_cinema(data, session)


@cinema_router.delete("/cinemas/{cinema_id}/delete", status_code=204)
async def drop_cinema(
    cinema_id: int,
    service: Annotated[CinemaService, Depends()],
    session: Annotated[session_transaction, Depends()],
):
    return await service.destroy_cinema(cinema_id, session)


@cinema_router.patch("/cinemas/{cinema_id}/update")
async def update_cinema(
    cinema_id: int,
    data: UpdateCinemaDTO,
    service: Annotated[CinemaService, Depends()],
    session: Annotated[session_transaction, Depends()],
):
    return await service.update_cinema(cinema_id, data, session)
