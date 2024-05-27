from dataclasses import asdict
from random import randint

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.logic import clear_none
from src.presentation.mappings import user as mapping
from src.presentation.mappings.main import data_mapper
from src.repository.user_repository import UserRepository
from src.service.impl.email_service_impl import EmailServiceimpl
from src.service.impl.redis_service_impl import RedisServiceImpl
from src.service.password_service import PasswordService
from src.service.user_service import UserService
from src.service.user_validate_service import UserValidateService


class UserServiceImpl(UserService):
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register(
        self,
        user_data: mapping.RegisterUserDto,
        password: PasswordService,
        validate: UserValidateService,
        email: EmailServiceimpl,
        session: AsyncSession,
    ) -> dict:

        user_dict = asdict(user_data)
        validate.validate_user(user_dict, password)

        user_dict["hashed_password"] = password.hashing(user_dict.pop("password1"))
        user_dict.pop("password2")

        user_id = await self.repo.create(user_dict, session)

        await email.send_verificated_message(user_dict.get("email"))

        return JSONResponse({"user_id": user_id}, status.HTTP_201_CREATED)

    async def fetch_users(self, session: AsyncSession):
        users = await self.repo.find_all(session)

        return {"user_list": data_mapper.dump(users, list[mapping.DetailProfileDto])}

    async def fetch_user_info(self, user_id: int, session: AsyncSession):
        user = await self.repo.find_by_id(user_id, session)
        user_dto = data_mapper.dump(user, mapping.DetailProfileDto)

        return {"user": user_dto}

    async def profile_page(self, user_id: int, session: AsyncSession):
        user = await self.repo.find_by_id(user_id, session)

        return {"profile": mapping.ProfileUserDto(user.nickname, user.email)}

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
        profile_dto = mapping.ProfileUserDto(updated_user.nickname, updated_user.email)
        return {"profile": profile_dto}

    async def set_password(
        self,
        user_id: int,
        pw: mapping.SetPasswordDto,
        session: AsyncSession,
        pw_service: PasswordService = PasswordService(),
    ):

        has_errors = pw_service.validate_password(pw.new_password1, pw.new_password2)

        if has_errors:
            raise HTTPException(400, has_errors)

        user = await self.repo.find_by_id(user_id, session)

        check_password = pw_service.verify(pw.old_password, user.hashed_password)

        if check_password is False:
            raise HTTPException(400, "incorrect old password")

        hashed_password = pw_service.hashing(pw.new_password1)

        await self.repo.update_password(user_id, hashed_password, session)

        return {"update": "ok"}

    async def recovery_password(
        self,
        email: str,
        redis: RedisServiceImpl,
        mail: EmailServiceimpl,
        session: AsyncSession,
    ):
        await self.repo.find_by_email(email, session)

        code = randint(1000, 9999)

        await redis.set_recovery_code(email, code)

        await mail.send_recovery_code(email, code)

        return {"ok": f"code {code} was send"}

    async def change_password(
        self,
        email: str,
        code: int,
        pw_data: mapping.NewPassowrdDto,
        password_service: PasswordService,
        redis: RedisServiceImpl,
        session: AsyncSession,
    ):
        if await redis.verify_code(email, str(code)) is False:
            raise HTTPException(400, "wrong code")

        user_instance = await self.repo.find_by_email(email, session)

        errors = password_service.validate_password(
            pw_data.password1, pw_data.password2
        )

        if errors:
            raise HTTPException(400, errors)

        hash_password = password_service.hashing(pw_data.password1)

        await self.repo.update_password(user_instance.id, hash_password, session)

        key = f"recovery:{email}"
        await redis.delete_key(key)
        return JSONResponse({"update": "success"}, status.HTTP_200_OK)
