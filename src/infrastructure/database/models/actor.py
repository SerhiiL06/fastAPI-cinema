from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Actor(Base):
    __tablename__ = "actors"

    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    birth_day: Mapped[date]
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))

    country: Mapped["Country"] = relationship(back_populates="actors")
    movies: Mapped[list["Movie"]] = relationship(
        secondary="MovieActors", back_populates="actors"
    )


class MovieActors(Base):
    __tablename__ = "movies_actors"

    actor_id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(primary_key=True)
