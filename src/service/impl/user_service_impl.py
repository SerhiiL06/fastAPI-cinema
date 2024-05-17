import re
from dataclasses import asdict

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.presentation.mappings.user import RegisterUserDto
from src.repository.user_repository import UserRepository
from src.service.password_service import PasswordService
from src.service.user_service import UserService


class UserServiceImpl(UserService):
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register(
        self,
        user_data: RegisterUserDto,
        session: AsyncSession,
        password: PasswordService = PasswordService(),
    ):

        self.validate_user(user_data, password)

        user_dict = asdict(user_data)
        user_dict["hashed_password"] = password.hashing(user_dict.pop("password1"))
        user_dict.pop("password2")
        user_id = await self.repo.create(user_dict, session)

        return {"user_id": user_id}

    @classmethod
    def validate_user(
        cls, data: RegisterUserDto, pw_service: PasswordService
    ) -> RegisterUserDto:
        errors = {}

        if not cls.is_correct_email(data.email) or len(data.email) > 320:
            errors["email"] = "error email pattern or length"

        if not cls.is_correct_nickname(data.nickname):
            errors["nickname"] = "nickname must have only letters and numbers"

        if not pw_service.compare(data.password1, data.password2):
            errors["password"] = "compare password error"

        is_incorrect_password = pw_service.validate_password(data.password1)

        if is_incorrect_password:
            errors["password_format"] = is_incorrect_password

        if errors:
            raise HTTPException(400, errors)

    @staticmethod
    def is_correct_email(email: str) -> bool:
        return bool(re.fullmatch(r"[a-z]{1,}@gmail.com", email))

    @staticmethod
    def is_correct_nickname(nickname: str) -> bool:
        return bool(re.findall(r"[A-Za-z0-9]{3,20}", nickname))

    async def fetch_users(self, session: AsyncSession):
        users = await self.repo.find_all(session)

        return users

    async def fetch_user_info(self, user_id: int, session: AsyncSession):
        user = await self.repo.find_by_id(user_id, session)

        return {"user": user}

    async def block_user(self, user_id, session: AsyncSession):
        block = {"is_active": False}
        await self.repo.update(user_id, block, session)
        return {"code": 200, "message": "blocked"}

    async def delete_user(self, user_id: int, session: AsyncSession) -> None:
        await self.repo.delete(user_id, session)

    async def update_profile(self, user_id: int, session: AsyncSession):
        return super().update_profile()
