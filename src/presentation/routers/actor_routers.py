from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.presentation.dependency import Container
from src.presentation.mappings.actor import CreateActorDto
from src.service.actor_service import ActorService

actor_routers = APIRouter(tags=["actors"])


@actor_routers.get("/actors")
@inject
async def actors_list(
    service: ActorService = Depends(Provide[Container.actor_service]),
):
    return await service.fetch_all()


@actor_routers.get("/actors/{actor_id}")
@inject
async def retrieve_actor(
    actor_id: int,
    service: ActorService = Depends(Provide[Container.actor_service]),
):
    return await service.fetch_by_id(actor_id)


@actor_routers.post("/actors")
@inject
async def create_actor(
    data: CreateActorDto,
    service: ActorService = Depends(Provide[Container.actor_service]),
):
    return await service.add_actor(data)
