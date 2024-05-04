from datetime import date, datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Movie(Base):
    __tablename__ = "movies"

    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(2500))
    image: Mapped[str] = mapped_column(nullable=True)
    release_date: Mapped[date]
    duration: Mapped[int]

    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    country_id: Mapped[int] = mapped_column(ForeignKey("actors.id"))

    categories: Mapped[list["Category"]] = relationship(
        secondary="MovieCategory", back_populates="movies"
    )
    actors: Mapped[list["Actor"]] = relationship(
        secondary="MovieActors", back_populates="movies"
    )

    country: Mapped["Country"] = relationship(back_populates="movies")
