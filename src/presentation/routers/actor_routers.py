from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from redis import Redis

from src.common.factories import current_user, session_factory
from src.presentation.dependency import Container
from src.presentation.mappings.actor import CreateActorDto
from src.service.actor_service import ActorService

actor_routers = APIRouter(tags=["actors"])


@actor_routers.get("/else")
@inject
async def something(
    service: Redis = Depends(Provide[Container.redis.provided.connection]),
):
    await service.set("test", 2)


@actor_routers.get("/actors")
@inject
async def actors_list(
    session: session_factory,
    service: ActorService = Depends(Provide[Container.actor_service]),
):
    return await service.fetch_all(session)


@actor_routers.get("/actors/{actor_id}")
@inject
async def retrieve_actor(
    session: session_factory,
    actor_id: int,
    service: ActorService = Depends(Provide[Container.actor_service]),
):
    return await service.fetch_by_id(actor_id, session)


@actor_routers.post("/actors")
@inject
async def create_actor(
    session: session_factory,
    data: CreateActorDto,
    service: ActorService = Depends(Provide[Container.actor_service]),
):
    return await service.add_actor(data, session)


@actor_routers.delete("/actors/{actor_id}")
@inject
async def drop_actor(
    session: session_factory,
    actor_id: int,
    service: ActorService = Depends(Provide[Container.actor_service]),
):
    return await service.delete_actor(actor_id, session)
