import string

from passlib.context import CryptContext


class PasswordService:
    __bcrypt = CryptContext(schemes="bcrypt")

    def validate_password(self, pw: str) -> dict:
        password_errors = {}

        if len(pw) < 8:
            password_errors["length"] = "password mush have min 8 length"

        checker = {"upper_case": 1, "punct": 1, "nums": 1}

        for el in pw:
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
