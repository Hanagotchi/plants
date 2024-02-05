from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.models.base import Base
from datetime import datetime
from typing import List

from app.schemas.Log import LogCreateSchema


class Log(Base):
    __tablename__ = "logs"
    __table_args__ = {'schema': 'dev'}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    title: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default="DEFAULT CURRENT_TIMESTAMP"
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default="DEFAULT CURRENT_TIMESTAMP"
    )
    content: Mapped[str] = mapped_column(String(1000))
    photos: Mapped[List["LogPhoto"]] = relationship(back_populates="log")

    def __repr__(self) -> str:
        return (
            f"Example(id={self.id}, "
            f"title={self.title}, "
            f"created_at={self.created_at}), "
            f"updated_at={self.updated_at}), "
            f"content={self.content}), "
            f"photos={self.photos}), "
        )

    @classmethod
    def from_pydantic(cls, pydantic_obj: LogCreateSchema):
        photos = list(map(lambda p: LogPhoto(
            photo_link=p.photo_link
        ), pydantic_obj.photos))
        return Log(
            title=pydantic_obj.title,
            content=pydantic_obj.content,
            photos=photos
        )


class LogPhoto(Base):
    __tablename__ = "logs_photos"
    __table_args__ = {'schema': 'dev'}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    photo_link: Mapped[str] = mapped_column(String(120))
    log_id: Mapped[int] = mapped_column(ForeignKey("dev.logs.id"))
    log: Mapped["Log"] = relationship(back_populates="photos")
