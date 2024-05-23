from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.logic import clear_none
from src.presentation.mappings.user import (DetailProfileDto, ProfileUserDto,
                                            RegisterUserDto)
from src.repository.user_repository import UserRepository
from src.service.password_service import PasswordService
from src.service.user_service import UserService
from src.service.user_validate_service import UserValidateService


class UserServiceImpl(UserService):
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register(
        self,
        user_data: RegisterUserDto,
        session: AsyncSession,
        password: PasswordService = PasswordService(),
        validate: UserValidateService = UserValidateService(),
    ):

        user_dict = asdict(user_data)
        validate.validate_user(user_dict, password)
        user_dict["hashed_password"] = password.hashing(user_dict.pop("password1"))
        user_dict.pop("password2")
        user_id = await self.repo.create(user_dict, session)

        return {"user_id": user_id}

    async def fetch_users(self, session: AsyncSession):
        users = await self.repo.find_all(session)

        return users

    async def fetch_user_info(self, user_id: int, session: AsyncSession):
        user = await self.repo.find_by_id(user_id, session)
        user_dto = DetailProfileDto(
            user.nickname,
            user.email,
            user.verificate,
            user.is_active,
            user.joined_at,
            user.role,
        )
        return {"user": user_dto}

    async def profile_page(self, user_id: int, session: AsyncSession):
        user = await self.repo.find_by_id(user_id, session)

        return {"profile": ProfileUserDto(user.nickname, user.email)}

    async def block_user(self, user_id, session: AsyncSession):
        block = {"is_active": False}
        await self.repo.update(user_id, block, session)
        return {"code": 200, "message": "blocked"}

    async def delete_user(self, user_id: int, session: AsyncSession) -> None:
        await self.repo.delete(user_id, session)

    async def update_profile(
        self,
        user_id: int,
        user_data: dict,
        session: AsyncSession,
        validate: UserValidateService = UserValidateService(),
    ):

        user_data = clear_none(user_data)
        validate.validate_user(user_data)

        updated_user = await self.repo.update(user_id, user_data, session)

        return {"profile": ProfileUserDto(updated_user.nickname, updated_user.email)}
