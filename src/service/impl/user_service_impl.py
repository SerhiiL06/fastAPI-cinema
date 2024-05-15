from src.repository.user_repository import UserRepository
from src.service.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from src.presentation.mappings.user import RegisterUserDto
from src.service.password_service import PasswordService
from dataclasses import asdict
import re


class UserServiceImpl(UserService):
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register(self, user_data: RegisterUserDto, session: AsyncSession):

        await self.repo.create()

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
