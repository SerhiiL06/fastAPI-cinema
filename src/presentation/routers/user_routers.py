from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.connections import session_transaction
from src.presentation.dependency import Container
from src.presentation.mappings.user import RegisterUserDto
from src.service.impl.user_service_impl import UserService, UserServiceImpl

users_router = APIRouter(tags=["users"])


@users_router.post("/register")
@inject
async def register(
    data: RegisterUserDto,
    session: Annotated[AsyncSession, Depends(session_transaction)],
    service: UserServiceImpl = Depends(Provide[Container.user_service]),
):
    return await service.register(data, session)
