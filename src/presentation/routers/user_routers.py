from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.common.factories import current_user, session_factory
from src.common.permissions import check_role
from src.presentation.dependency import Container
from src.presentation.mappings.user import RegisterUserDto
from src.service.impl.auth_service import AuthService
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
