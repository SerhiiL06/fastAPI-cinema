from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"

    nickname: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(320), unique=True)

    verificate: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    joined_at: Mapped[datetime] = mapped_column(default=datetime.now())

    role: Mapped[str] = mapped_column(default="regular")

    def __repr__(self) -> str:
        return self.nickname
