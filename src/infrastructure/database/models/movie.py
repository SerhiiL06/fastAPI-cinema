from .base import Base
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import String, ForeignKey


class Movie(Base):
    __tablename__ = "movies"

    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(2500))
    image: Mapped[str] = mapped_column(nullable=True)

    country_id: Mapped[int] = mapped_column(ForeignKey("actors.id"))

    categories: Mapped[list["Category"]] = relationship(
        secondary="MovieCategory", back_populates="movies"
    )
    actors: Mapped[list["Actor"]] = relationship(
        secondary="MovieActors", back_populates="movies"
    )

    country: Mapped["Country"] = relationship(back_populates="movies")
