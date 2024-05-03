from .base import Base
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import String


class Country(Base):
    __tablename__ = "countries"

    iso: Mapped[str]
    name: Mapped[str]

    movies: Mapped[list["Movie"]] = relationship(back_populates="country")
    actors: Mapped[list["Actor"]] = relationship(back_populates="country")
