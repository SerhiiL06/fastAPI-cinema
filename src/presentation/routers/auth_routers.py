from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.common.factories import session_factory
from src.presentation.dependency import Container
from src.service.impl.auth_service import AuthService

auth_routers = APIRouter(prefix="/auth", tags=["auth"])


@auth_routers.post("/login", tags=["auth"])
@inject
async def login(
    session: session_factory,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthService = Depends(Provide[Container.auth_service]),
):

    return await service.login(form_data.username, form_data.password, session)
