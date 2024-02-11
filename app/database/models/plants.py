from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.models.base import Base
from app.schemas.plants import PlantsSchema


class Plants(Base):
    __tablename__ = "plants"
    __table_args__ = {'schema': 'dev'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    scientific_name: Mapped[str] = mapped_column(String(64), nullable=False)

    def __repr__(self) -> str:
        return (f"Example(id={self.id!r}, user_id={self.user_id!r}, "
                f"name={self.name!r}, scientific_name={self.scientific_name!r})")

    @classmethod
    def from_pydantic(cls, pydantic_obj: PlantsSchema):
        return Plants(
            id=pydantic_obj.id,
            user_id=pydantic_obj.user_id,
            name=pydantic_obj.name,
            scientific_name=pydantic_obj.scientific_name
        )
