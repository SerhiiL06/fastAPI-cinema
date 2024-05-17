from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.connections import session_transaction
from src.presentation.dependency import Container, auth
from src.presentation.mappings.user import RegisterUserDto
from src.service.impl.auth_service import AuthService
from src.service.impl.user_service_impl import UserServiceImpl

users_router = APIRouter(tags=["users"])


@users_router.post("/register")
@inject
async def register(
    data: RegisterUserDto,
    session: Annotated[AsyncSession, Depends(session_transaction)],
    service: UserServiceImpl = Depends(Provide[Container.user_service]),
):
    return await service.register(data, session)


@users_router.get("/users")
@inject
async def register(
    session: Annotated[AsyncSession, Depends(session_transaction)],
    service: UserServiceImpl = Depends(Provide[Container.user_service]),
):
    return await service.fetch_users(session)


@users_router.post("/users/login")
@inject
async def login(
    session: Annotated[AsyncSession, Depends(session_transaction)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthService = Depends(Provide[Container.auth_service]),
):

    return await service.login(form_data.username, form_data.password, session)


@users_router.get("/testing")
async def some(
    current_user: Annotated[dict, Depends(auth.authenticate)],
):
    print(current_user)
