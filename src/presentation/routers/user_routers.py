from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.common.factories import current_user, session_factory
from src.common.permissions import check_role
from src.presentation.dependency import Container
from src.presentation.mappings.user import RegisterUserDto
from src.service.impl.comment_service_impl import CommentServiceImpl
from src.service.impl.user_service_impl import UserServiceImpl

users_router = APIRouter(tags=["users"])


@users_router.post("/register")
@inject
async def register(
    data: RegisterUserDto,
    session: session_factory,
    service: UserServiceImpl = Depends(Provide[Container.user_service]),
):
    return await service.register(data, session)


@users_router.get("/users")
@inject
async def user_list(
    session: session_factory,
    service: UserServiceImpl = Depends(Provide[Container.user_service]),
):
    return await service.fetch_users(session)


@users_router.get("/profile")
@inject
async def my_profile(
    user: current_user,
    session: session_factory,
    service: UserServiceImpl = Depends(Provide[Container.user_service]),
):
    return await service.profile_page(user.get("user_id"), session)


@users_router.get("/{user_id}/profile")
@check_role(["regular"])
@inject
async def user_info(
    user: current_user,
    user_id: int,
    session: session_factory,
    service: UserServiceImpl = Depends(Provide[Container.user_service]),
):
    return await service.fetch_user_info(user_id, session)


@users_router.get("/users/comments")
@check_role(["regular"])
@inject
async def fetch_user_comments(
    user: current_user,
    user_id: int,
    session: session_factory,
    service: CommentServiceImpl = Depends(Provide[Container.comment_service]),
):
    return await service.user_comments(user_id, session)
