from typing import Annotated

from fastapi import APIRouter, Depends

from src.infrastructure.database.connections import session_transaction
from src.presentation.mappings.cinema import CinemaDTO, CityDTO
from src.repository.cinema_repository import CinemaRepository
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
