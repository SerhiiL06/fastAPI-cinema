import string
from random import randint

from passlib.context import CryptContext


class PasswordService:
    __bcrypt = CryptContext(schemes="bcrypt")

    def validate_password(self, pw1: str, pw2: str) -> dict:
        password_errors = {}

        if not self.compare(pw1, pw2):
            password_errors["password"] = "compare password error"
            return password_errors

        if len(pw1) < 8:
            password_errors["length"] = "password mush have min 8 length"

        checker = {"upper_case": 1, "punct": 1, "nums": 1}

        for el in pw1:
            if el.isupper():
                checker["upper_case"] -= 1
            elif el in string.punctuation:
                checker["punct"] -= 1
            elif el.isdigit():
                checker["nums"] -= 1

        for k, v in checker.items():
            if v > 0:
                password_errors[k] = f"{k} must be at least one character"

        return password_errors

    def compare(self, first: str, second: str) -> bool:
        return first == second

    def hashing(self, pw: str) -> str:
        return self.__bcrypt.hash(pw)

    def verify(self, secret: str, hashed: str) -> bool:
        return self.__bcrypt.verify(secret, hashed)

    @staticmethod
    def generate_recovery_code() -> int:
        return randint(1000, 9999)
