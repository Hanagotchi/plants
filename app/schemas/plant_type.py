from pydantic import BaseModel, Field


class PlantTypeSchema(BaseModel):
    botanical_name: str = Field(..., max_length=70)
    common_name: str = Field(..., max_length=70)
    description: str = Field(..., max_length=600)
    cares: str = Field(..., max_length=600)
    photo_link: str = Field(..., max_length=120)

    class Config:
        json_schema_extra = {
            "example": {
                "botanical_name": "Streptocarpus",
                "common_name": "Cabo Primrose",
                "description": "Su nombre común es Cabo Primrose, refiriéndose...",
                "cares": "Se desempeña mejor con luz brillante filtrada y...",
                "photo_link": "https://www.whiteflowerfarm.com/mas_assets/cache/image/3/e/e/2/16098.Jpg"
            }
        }