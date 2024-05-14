from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.connections import session_transaction
from src.presentation.dependency import Container
from src.presentation.mappings.actor import CreateActorDto
from src.service.actor_service import ActorService

actor_routers = APIRouter(tags=["actors"])


@actor_routers.get("/actors")
@inject
async def actors_list(
    session: Annotated[AsyncSession, Depends(session_transaction)],
    service: ActorService = Depends(Provide[Container.actor_service]),
):
    return await service.fetch_all(session)


@actor_routers.get("/actors/{actor_id}")
@inject
async def retrieve_actor(
    session: Annotated[AsyncSession, Depends(session_transaction)],
    actor_id: int,
    service: ActorService = Depends(Provide[Container.actor_service]),
):
    return await service.fetch_by_id(actor_id, session)


@actor_routers.post("/actors")
@inject
async def create_actor(
    session: Annotated[AsyncSession, Depends(session_transaction)],
    data: CreateActorDto,
    service: ActorService = Depends(Provide[Container.actor_service]),
):
    return await service.add_actor(data, session)


@actor_routers.delete("/actors/{actor_id}")
@inject
async def drop_actor(
    session: Annotated[AsyncSession, Depends(session_transaction)],
    actor_id: int,
    service: ActorService = Depends(Provide[Container.actor_service]),
):
    return await service.delete_actor(actor_id, session)
