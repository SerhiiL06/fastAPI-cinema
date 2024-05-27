import re

from email_validator import validate_email
from fastapi import HTTPException

from src.service.password_service import PasswordService


class UserValidateService:

    def validate_user(self, data: dict, pw_service: PasswordService = None):

        errors = {}

        email = data.get("email")
        nickname = data.get("nickname")
        password1 = data.get("password1")
        password2 = data.get("password2")
        validate_email(email)
        if email and not self.is_correct_email(email):
            errors["email"] = "error email pattern or length"

        if nickname and not self.is_correct_nickname(nickname):
            errors["nickname"] = "nickname must have only letters and numbers"

        password_errors = None
        if password1:
            password_errors = pw_service.validate_password(password1, password2)

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
