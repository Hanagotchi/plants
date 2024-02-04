from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.models.base import Base


class PlantType(Base):
    __tablename__ = "plant_types"
    __table_args__ = {'schema': 'dev'}

    botanical_name: Mapped[str] = mapped_column(String(70), primary_key=True)
    common_name: Mapped[str] = mapped_column(String(70))
    description: Mapped[str] = mapped_column(String(500))
    cares: Mapped[str] = mapped_column(String(500))
    photo_link: Mapped[str] = mapped_column(String(120))

    def __repr__(self) -> str:
        return (f"PlantType(botanical_name={self.botanical_name}, "
                f"common_name={self.common_name}, "
                f"description={self.description}), "
                f"cares={self.cares}), "
                f"age={self.photo_link})")
