from passlib.context import CryptContext
import string
import re


class PasswordService:
    __bcrypt = CryptContext(schemes="bcrypt")

    def validate_password(self, pw: str) -> dict | None:
        password_errors = {}

        if len(pw) < 8:
            password_errors["password mush have min 8 length"]

        checker = {"upper": 1, "spec": 1, "nums": 1}
        for el in pw:
            if el.isupper():
                checker["upper"] -= 1
            elif el in string.punctuation:
                checker["spec"] -= 1

    def compare(self, firts: str, second: str):
        return firts == second

    def hashing(self, pw: str):
        return self.__bcrypt.hash(pw)

    def verify(self, new: str, old: str) -> str:
        new_pw = self.__bcrypt.verify_and_update(new, old)
        return new_pw
