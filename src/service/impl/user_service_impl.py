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

    async def register(self, user_data: RegisterUserDto, session: AsyncSession):
        self.validate_user(user_data)
        await self.repo.create(asdict(user_data), session)

    @classmethod
    def validate_user(
        cls, data: RegisterUserDto, pw_service: PasswordService = PasswordService()
    ) -> RegisterUserDto:
        errors = {}

        if not re.findall(r"\w+@[a-z]/.com", data.email) or len(data.email) > 320:
            errors["email"] = "error email pattern or length"

        if not re.findall(r"\w{3,20}", data.nickname):
            errors["nickname"] = "nickname must have only letters and numbers"

        if pw_service.compare(data.password1, data.password2):
            errors["password"] = "compare password error"

        if errors:
            raise HTTPException(400, errors)

        password_incorrect = pw_service.validate_password(data.password1)

        if password_incorrect:
            raise HTTPException(400, password_incorrect)
