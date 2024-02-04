from typing import List
from fastapi import APIRouter, Request, status, Query
from app.controller import plant_types_controller as controller
from app.schemas.plant_type import PlantTypeSchema

plant_type = APIRouter()


@plant_type.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[PlantTypeSchema]
)
async def get_all_plant_types(req: Request, limit: int = Query(10)):
    return controller.get_all_plant_types(req, limit)


@plant_type.get(
    "/{botanical_name}",
    status_code=status.HTTP_200_OK,
    response_model=PlantTypeSchema
)
async def get_plant_type(
    botanical_name: str,
    req: Request,
):
    return controller.get_plant_type(req, botanical_name)
