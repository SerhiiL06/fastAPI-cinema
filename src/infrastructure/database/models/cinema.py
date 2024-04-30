from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class City(Base):
    __tablename__ = "cities"
    title: Mapped[str] = mapped_column(unique=True)

    cinemas: Mapped[List["Cinema"]] = relationship(back_populates="city", cascade="")


class Cinema(Base):
    __tablename__ = "cinemas"

    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(100), nullable=True)

    phone_number: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(150))

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    street: Mapped[str] = mapped_column(String(150))
    house_number: Mapped[int]

    city: Mapped["City"] = relationship(back_populates="cinemas", lazy="selectin")
