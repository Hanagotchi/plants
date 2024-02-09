from pydantic import BaseModel, Field


class PlantSchema(BaseModel):
    id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    name: str = Field(..., example="Agus")
    scientific_name: str = Field(..., example="Aguspolis grandis")
