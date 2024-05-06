from datetime import date, datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Category(Base):
    __tablename__ = "categories"

    title: Mapped[str] = mapped_column(String(30), unique=True)

    movies: Mapped[list["Movie"]] = relationship(
        secondary="movies_category", back_populates="categories"
    )


class MovieCategory(Base):
    __tablename__ = "movies_category"
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), primary_key=True
    )
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)


class Country(Base):
    __tablename__ = "countries"

    iso: Mapped[str]
    name: Mapped[str]

    movies: Mapped[list["Movie"]] = relationship(back_populates="country")
    actors: Mapped[list["Actor"]] = relationship(back_populates="country")


class MovieActors(Base):
    __tablename__ = "movies_actors"

    actor_id: Mapped[int] = mapped_column(ForeignKey("actors.id"), primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)


class Actor(Base):
    __tablename__ = "actors"

    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    birth_day: Mapped[date]
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    movies: Mapped[list["Movie"]] = relationship(
        "Movie", secondary="movies_actors", back_populates="actors"
    )
    country = relationship(Country, back_populates="actors")


class Movie(Base):
    __tablename__ = "movies"

    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(2500))
    image: Mapped[str] = mapped_column(nullable=True)
    release_date: Mapped[date]
    duration: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))

    actors: Mapped[list[Actor]] = relationship(
        secondary="movies_actors", back_populates="movies"
    )

    categories: Mapped[list["Category"]] = relationship(
        secondary="movies_category", back_populates="movies"
    )

    country: Mapped["Country"] = relationship(back_populates="movies")
