from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.user_repository import UserRepository
from src.service.impl.token_service import TokenService
from src.service.password_service import PasswordService

bearer = OAuth2PasswordBearer(tokenUrl="auth/login")


class AuthService:

    def __init__(
        self, repo: UserRepository, pswd: PasswordService, token: TokenService
    ) -> None:
        self.repo = repo
        self.pswd = pswd
        self.token = token

    async def login(self, nickname: str, password: str, session: AsyncSession) -> dict:
        instance = await self.repo.find_by_nickname(nickname, session)

        if self.pswd.verify(password, instance.hashed_password) is False:
            raise HTTPException(401, "wrong password or email")

        if not instance.is_active:
            raise HTTPException(401, "Your account is not active")

        payload = {
            "user_id": instance.id,
            "email": instance.email,
            "role": instance.role,
        }
        token = self.token.create_token(payload)
        return token

    def authenticate(self, token: Annotated[str, Depends(bearer)]):

        user_data = self.token.get_token(token)
        return user_data
