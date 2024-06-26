from dataclasses import asdict

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from fastapi_limiter.depends import RateLimiter

from src.common.factories import current_user, session_factory
from src.common.permissions import check_role
from src.presentation.dependency import Container
from src.presentation.mappings import user as user_mapping
from src.service.impl.comment_service_impl import CommentServiceImpl
from src.service.impl.email_service_impl import EmailServiceimpl
from src.service.impl.redis_service_impl import RedisServiceImpl
from src.service.impl.user_service_impl import UserServiceImpl
from src.service.password_service import PasswordService
from src.service.user_validate_service import UserValidateService

users_router = APIRouter(tags=["users"])


@users_router.post("/register")
@inject
async def register(
    data: user_mapping.RegisterUserDto,
    session: session_factory,
    service: UserServiceImpl = Depends(Provide[Container.user_service]),
    password_service: PasswordService = Depends(Provide[Container.password_service]),
    validate_service: UserValidateService = Depends(UserValidateService),
    email: EmailServiceimpl = Depends(Provide[Container.email_service]),
):
    return await service.register(
        data, password_service, validate_service, email, session
    )


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


@users_router.patch("/profile")
@inject
async def update_profile(
    user: current_user,
    data: user_mapping.UpdateProfileDto,
    session: session_factory,
    service: UserServiceImpl = Depends(Provide[Container.user_service]),
):
    return await service.update_profile(user.get("user_id"), asdict(data), session)


@users_router.patch("/profile/set-password")
@inject
async def change_password(
    user: current_user,
    data: user_mapping.SetPasswordDto,
    session: session_factory,
    service: UserServiceImpl = Depends(Provide[Container.user_service]),
):
    return await service.set_password(user.get("user_id"), data, session)


@users_router.post(
    "/users/forgot-password", dependencies=[Depends(RateLimiter(1, minutes=1))]
)
@inject
async def forgot_password(
    request: Request,
    email: str,
    session: session_factory,
    service: UserServiceImpl = Depends(Provide[Container.user_service]),
    redis_service: RedisServiceImpl = Depends(Provide[Container.redis_service]),
    email_service: EmailServiceimpl = Depends(Provide[Container.email_service]),
):
    return await service.recovery_password(email, redis_service, email_service, session)


@users_router.post("/users/recovery/{email}")
@inject
async def restore_password(
    email: str,
    code: int,
    password_data: user_mapping.NewPassowrdDto,
    session: session_factory,
    service: UserServiceImpl = Depends(Provide[Container.user_service]),
    password_service: PasswordService = Depends(Provide[Container.password_service]),
    redis_service: RedisServiceImpl = Depends(Provide[Container.redis_service]),
):
    return await service.change_password(
        email, code, password_data, password_service, redis_service, session
    )


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


@users_router.delete("/users/delete")
@check_role(["regular"])
@inject
async def update_profile(
    user: current_user,
    user_id: int,
    session: session_factory,
    service: UserServiceImpl = Depends(Provide[Container.user_service]),
):
    return await service.delete_user(user_id, session)


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
