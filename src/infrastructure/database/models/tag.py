from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .movie import Movie


class Tag(Base):
    __tablename__ = "tags"

    title: Mapped[str] = mapped_column(String(50), unique=True)

    movies = relationship("Movie", secondary="movies_tags", back_populates="tags")


class MovieTags(Base):
    __tablename__ = "movies_tags"

    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
