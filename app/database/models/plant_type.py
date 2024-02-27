from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database.models.base import Base
from app.schemas.plant_type import PlantTypeSchema


class PlantType(Base):
    __tablename__ = "plant_types"
    __table_args__ = {'schema': 'dev'}

    botanical_name: Mapped[str] = mapped_column(String(70), primary_key=True)
    id: Mapped[int] = mapped_column(Integer, nullable=False)
    common_name: Mapped[str] = mapped_column(String(70))
    description: Mapped[str] = mapped_column(String(600))
    cares: Mapped[str] = mapped_column(String(600))
    photo_link: Mapped[str] = mapped_column(String(120))

    def __repr__(self) -> str:
        return (f"PlantType(botanical_name={self.botanical_name}, "
                f"id={self.id}, "
                f"common_name={self.common_name}, "
                f"description={self.description}), "
                f"cares={self.cares}), "
                f"age={self.photo_link})")

    @classmethod
    def from_pydantic(cls, pydantic_obj: PlantTypeSchema):
        return PlantType(
            botanical_name=pydantic_obj.botanical_name,
            id=pydantic_obj.id,
            common_name=pydantic_obj.common_name,
            description=pydantic_obj.description,
            cares=pydantic_obj.cares,
            photo_link=pydantic_obj.photo_link
        )
