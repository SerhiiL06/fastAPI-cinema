from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import Base


class MovieRating(Base):
    __tablename__ = "movies_rating"

    __table_args__ = (UniqueConstraint("movie_id", "user_id", name="mov_rat_1"),)

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    rating: Mapped[int]
