from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.models.base import Base
from datetime import datetime
from typing import List


class Log(Base):
    __tablename__ = "logs"
    __table_args__ = {'schema': 'dev'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    post_date: Mapped[datetime] = mapped_column(DateTime)
    last_update_date: Mapped[datetime] = mapped_column(DateTime)
    content: Mapped[str] = mapped_column(String(1000))
    photos: Mapped[List["LogPhoto"]] = relationship(back_populates="logphoto")

    def __repr__(self) -> str:
        return (
            f"Example(id={self.id}, "
            f"title={self.title}, "
            f"post_date={self.post_date}), "
            f"last_update_date={self.lastupdate_date}), "
            f"content={self.content}), "
        )


class LogPhoto(Base):
    __tablename__ = "logs_photos"
    __table_args__ = {'schema': 'dev'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    photo_link: Mapped[str] = mapped_column(String(120))
    log_id: Mapped[int] = mapped_column(ForeignKey("logs.id"))
    log: Mapped["Log"] = relationship(back_populates="log")
