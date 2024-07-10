from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import Base


class MovieRating(Base):
    __tablename__ = "movies_rating"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    rating: Mapped[int]
