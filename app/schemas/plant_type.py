from pydantic import BaseModel, Field

link = ("https://www.whiteflowerfarm.com"
        "/mas_assets/cache/image/3/e/e/2/16098.Jpg")


class PlantTypeSchema(BaseModel):
    botanical_name: str = Field(..., max_length=70)
    id: int = Field(..., gt=0)
    common_name: str = Field(..., max_length=70)
    description: str = Field(..., max_length=1000)
    cares: str = Field(..., max_length=1000)
    photo_link: str = Field(..., max_length=300)

    class Config:
        json_schema_extra = {
            "example": {
                "botanical_name": "Streptocarpus",
                "id": 224,
                "common_name": "Cabo Primrose",
                "description": ("Su nombre común es Cabo Primrose, "
                                "refiriéndose..."),
                "cares": "Se desempeña mejor con luz brillante filtrada y...",
                "photo_link": link
            }
        }
