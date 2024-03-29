from typing import List
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.schemas.plant import PlantCreateSchema
from os import environ

SCHEMA = environ.get("POSTGRES_SCHEMA", "plants_service")


class Plant(Base):
    __tablename__ = "plants"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
        )
    id_user: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    scientific_name: Mapped[str] = mapped_column(
        ForeignKey(f"{SCHEMA}.plant_types.botanical_name")
    )
    logs: Mapped[List["Log"]] = relationship( # noqa F821
        back_populates="plant", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return (
            f"Plant(id={self.id!r}, id_user={self.id_user!r}, "
            f"name={self.name!r}, scientific_name={self.scientific_name!r})"
        )

    @classmethod
    def from_pydantic(cls, pydantic_obj: PlantCreateSchema):
        return Plant(
            id_user=pydantic_obj.id_user,
            name=pydantic_obj.name,
            scientific_name=pydantic_obj.scientific_name,
            logs=[],
        )
