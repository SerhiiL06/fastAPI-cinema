from typing import Annotated

from fastapi import APIRouter, Depends

from src.infrastructure.database.connections import session_transaction
from src.presentation.mappings.cinema import CinemaDTO, CityDTO
from src.service.cinema_service import CinemaService

cinema_router = APIRouter()


@cinema_router.post("/create")
async def post_city(
    data: CityDTO,
    service: Annotated[CinemaService, Depends()],
    session: Annotated[session_transaction, Depends()],
):
    return await service.add_city(data, session)


@cinema_router.post("/cinema")
async def post_cinema(
    data: CinemaDTO,
    service: Annotated[CinemaService, Depends()],
    session: Annotated[session_transaction, Depends()],
):
    return await service.add_cinema(data, session)


@cinema_router.get("/cinema")
async def fetch_cinemas(
    service: Annotated[CinemaService, Depends()],
    session: Annotated[session_transaction, Depends()],
):
    return await service.get_cinema_list(session)


@cinema_router.get("/cinema/{cinema_id}")
async def detail_cinema(
    cinema_id: int,
    service: Annotated[CinemaService, Depends()],
    session: Annotated[session_transaction, Depends()],
):
    return await service.get_cinema(cinema_id, session)


@cinema_router.delete("/cinema/{cinema_id}")
async def drop_cinema(
    cinema_id: int,
    service: Annotated[CinemaService, Depends()],
    session: Annotated[session_transaction, Depends()],
):
    return await service.destroy_cinema(cinema_id, session)
