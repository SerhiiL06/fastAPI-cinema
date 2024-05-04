from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Country(Base):
    __tablename__ = "countries"

    iso: Mapped[str]
    name: Mapped[str]

    movies: Mapped[list["Movie"]] = relationship(back_populates="country")
    actors: Mapped[list["Actor"]] = relationship(back_populates="country")
