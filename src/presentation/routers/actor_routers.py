from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.presentation.dependency import Container
from src.service.actor_service import ActorService

actor_routers = APIRouter(tags=["actors"])


@actor_routers.get("/actors")
@inject
async def actors_list(
    service: ActorService = Depends(Provide[Container.actor_service]),
):
    return await service.fetch_all()
