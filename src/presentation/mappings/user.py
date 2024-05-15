from dataclasses import dataclass


@dataclass
class RegisterUserDto:
    email: str
    nickname: str

    password1: str
    password2: str
