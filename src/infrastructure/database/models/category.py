from .base import Base
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import String


class Category(Base):
    __tablename__ = "categories"

    title: Mapped[str] = mapped_column(String(30), unique=True)

    movies: Mapped[list["Movie"]] = relationship(
        secondary="MovieCategory", back_populates="categories"
    )


class MovieCategory(Base):
    __tablename__ = "movies_category"
    category_id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(primary_key=True)
