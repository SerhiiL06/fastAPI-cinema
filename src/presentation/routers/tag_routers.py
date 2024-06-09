from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends

from src.common.factories import current_user, session_factory
from src.common.permissions import check_role
from src.presentation.dependency import Container
from src.presentation.mappings.tag import TagDto
from src.service.impl.tag_service_impl import TagServiceImpl

tag_router = APIRouter(prefix="/tags", tags=["tags"])


@tag_router.get("")
@check_role(["regular"])
@inject
async def tags_list(
    session: session_factory,
    user: current_user,
    service: TagServiceImpl = Depends(Provide[Container.tag_service]),
):
    return await service.fetch_tags(session)


@tag_router.post("")
@check_role(["regular"])
@inject
async def add_tag(
    session: session_factory,
    user: current_user,
    tag_info: TagDto,
    service: TagServiceImpl = Depends(Provide[Container.tag_service]),
):
    return await service.create_tag(tag_info, session)


@tag_router.get("/{tag_id}")
@check_role(["regular"])
@inject
async def retrieve_tag(
    session: session_factory,
    tag_id: int,
    user: current_user,
    service: TagServiceImpl = Depends(Provide[Container.tag_service]),
):
    return await service.fetch_tag_info(tag_id, session)


@tag_router.patch("/{tag_id}")
@check_role(["regular"])
@inject
async def update_tag(
    session: session_factory,
    tag_id: int,
    tag_info: TagDto,
    user: current_user,
    service: TagServiceImpl = Depends(Provide[Container.tag_service]),
):
    return await service.update_tag(tag_id, tag_info, session)


@tag_router.delete("/{tag_id}")
@check_role(["regular"])
@inject
async def delete_tag(
    session: session_factory,
    tag_id: int,
    user: current_user,
    service: TagServiceImpl = Depends(Provide[Container.tag_service]),
):
    return await service.drop_tag(tag_id, session)
