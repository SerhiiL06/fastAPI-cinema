from dataclasses import dataclass
from datetime import datetime


@dataclass
class RegisterUserDto:
    email: str
    nickname: str

    password1: str
    password2: str


@dataclass
class ProfileUserDto:
    nickname: str
    email: str


@dataclass
class UpdateProfileDto:
    nickname: str = None
    email: str = None


@dataclass
class DetailProfileDto(ProfileUserDto):
    verificate: bool
    is_active: bool
    joined_at: datetime
    role: str


@dataclass
class SetPasswordDto:
    old_password: str
    new_password1: str
    new_password2: str


@dataclass
class NewPassowrdDto:
    password1: str
    password2: str
