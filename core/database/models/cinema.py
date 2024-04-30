from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey


class City(Base):
    __tablename__ = "cities"
    title: Mapped[str] = mapped_column(unique=True)


class Cinema(Base):
    __tablename__ = "cinemas"

    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(100), nullable=True)

    phone_number: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(150))

    city_id: Mapped["City"] = mapped_column(ForeignKey("cities.id"))
    street: Mapped[str] = mapped_column(String(150))
    house_number: Mapped[int]
