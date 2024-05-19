from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.common.factories import current_user, session_factory
from src.presentation.dependency import Container
from src.presentation.mappings.user import RegisterUserDto
from src.service.impl.auth_service import AuthService
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
async def register(
    session: session_factory,
    service: UserServiceImpl = Depends(Provide[Container.user_service]),
):
    return await service.fetch_users(session)


@users_router.post("/users/login", tags=["auth"])
@inject
async def login(
    session: session_factory,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthService = Depends(Provide[Container.auth_service]),
):

    return await service.login(form_data.username, form_data.password, session)
