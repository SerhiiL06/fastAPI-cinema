from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Comment(Base):

    __tablename__ = "comments"

    text: Mapped[str] = mapped_column(String(250))

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"))

    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    movie = relationship("Movie", back_populates="comments", single_parent=True)

    author = relationship("User", back_populates="comments", single_parent=True)
