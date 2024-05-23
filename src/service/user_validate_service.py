from src.presentation.mappings.user import RegisterUserDto
from src.service.password_service import PasswordService
import re
from fastapi import HTTPException


class UserValidateService:

    def validate_user(
        self, data: RegisterUserDto, pw_service: PasswordService
    ) -> RegisterUserDto:

        errors = {}

        if not self.is_correct_email(data.email):
            errors["email"] = "error email pattern or length"

        if not self.is_correct_nickname(data.nickname):
            errors["nickname"] = "nickname must have only letters and numbers"

        password_errors = pw_service.validate_password(data.password1, data.password2)

        if password_errors:
            errors["password_format"] = password_errors

        if errors:
            raise HTTPException(400, errors)

    @staticmethod
    def is_correct_email(email: str) -> bool:
        return bool(re.fullmatch(r"[a-z]{1,}@gmail.com", email)) and len(email) < 320

    @staticmethod
    def is_correct_nickname(nickname: str) -> bool:
        return bool(re.findall(r"[A-Za-z0-9]{3,20}", nickname))
