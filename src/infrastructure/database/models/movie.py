from datetime import date, datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

from .comments import Comment


class Genre(Base):
    __tablename__ = "genres"

    title: Mapped[str] = mapped_column(String(30), unique=True)

    movies: Mapped[list["Movie"]] = relationship(
        secondary="movies_genre", back_populates="genres"
    )


class MovieGenre(Base):
    __tablename__ = "movies_genre"
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), primary_key=True)
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
    slug: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(String(2500))
    image: Mapped[str] = mapped_column(nullable=True)
    release_date: Mapped[date]
    duration: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    is_publish: Mapped[bool] = mapped_column(default=True)

    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))

    actors: Mapped[list[Actor]] = relationship(
        secondary="movies_actors", back_populates="movies"
    )

    genres: Mapped[list["Genre"]] = relationship(
        secondary="movies_genre", back_populates="movies"
    )
    comments: Mapped[list["Comment"]] = relationship(back_populates="movie")
    country: Mapped["Country"] = relationship(back_populates="movies")
