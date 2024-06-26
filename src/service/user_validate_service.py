import re

import email_validator
from email_validator import validate_email
from fastapi import HTTPException

from src.service.password_service import PasswordService


class UserValidateService:

    def validate_user(self, data: dict, pw_service: PasswordService = None) -> None:

        errors = {}

        email = data.get("email")
        nickname = data.get("nickname")
        password1 = data.get("password1")
        password2 = data.get("password2")

        try:
            validate_email(email)
        except email_validator.EmailSyntaxError as _:
            raise HTTPException(400, "Check the email pattern")

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
    def is_correct_nickname(nickname: str) -> bool:
        return bool(re.findall(r"[A-Za-z0-9]{3,20}", nickname))
