from pydantic import BaseModel, Field
from typing import Optional


class ExampleSchema(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    age: int = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "name": "Agus",
                "age": 25
            }
        }


class ExampleUpdateSchema(BaseModel):
    name: str = Field(...)
    age: int = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Agus",
                "age": 35
            }
        }


class ExamplePartialUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Agus",
                "age": 35
            }
        }
