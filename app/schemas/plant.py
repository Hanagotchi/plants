from pydantic import BaseModel, Field


class PlantCreateSchema(BaseModel):
    id_user: int = Field(..., example=1)
    name: str = Field(..., example="Agus")
    scientific_name: str = Field(..., example="Thunbergia alata")


class PlantSchema(PlantCreateSchema):
    id: int = Field(..., example=1)
