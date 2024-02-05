from sqlalchemy import Integer, String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.database.models.base import Base
from app.schemas.example import ExampleSchema


class Example(Base):
    __tablename__ = "examples1"
    __table_args__ = {'schema': 'dev'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    age: Mapped[int] = mapped_column(SmallInteger)

    def __repr__(self) -> str:
        return (f"Example(id={self.id}, name={self.name}, age={self.age})")

    @classmethod
    def from_pydantic(cls, pydantic_obj: ExampleSchema):
        return Example(
            id=pydantic_obj.id,
            name=pydantic_obj.name,
            age=pydantic_obj.age
        )
