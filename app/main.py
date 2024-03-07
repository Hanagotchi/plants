from fastapi import FastAPI, Request, Response, status, Query, Body
from app.controller.Plants import PlantController
import logging
from typing import Optional
from app.repository.Plants import PlantsDB
from app.schemas.Log import (
    LogCreateSchema,
    LogPartialUpdateSchema,
    LogPhotoCreateSchema,
)
from app.schemas.plant import (
    PlantCreateSchema
)
from app.service.Plants import PlantsService

tags_metadata = [
    {"name": "Plants", "description": "Operations with plants."},
]

app = FastAPI(
    openapi_tags=tags_metadata,
    title="Plants API",
    version="0.1.0",
    summary="Microservice for plants management",
)

plants_repository = PlantsDB()
plants_service = PlantsService(plants_repository)
plants_controller = PlantController(plants_service)

logger = logging.getLogger("plants")
logger.setLevel("DEBUG")


@app.on_event("startup")
async def start_up():
    app.logger = logger

    try:
        app.logger.info("Postgres connection established")
    except Exception as e:
        app.logger.error(e)
        app.logger.error("Could not connect to Postgres client")


@app.on_event("shutdown")
async def shutdown_db_client():
    plants_repository.shutdown()
    app.logger.info("Postgres shutdown succesfully")


@app.post(
    "/plants",
    tags=["Plants"],
    responses={
        status.HTTP_200_OK: {
            "description": "Return the plant successfully created."
        },
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid request body"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error"
        },
    },
)
async def create_plant(item: PlantCreateSchema):
    return plants_controller.handle_create_plant(item)


@app.get("/plants", tags=["Plants"])
async def get_all_plants(id_user: int = Query(None), limit: int = Query(1024)):
    if id_user is not None:
        return plants_controller.handle_get_plants_by_user(id_user, limit)

    return plants_controller.handle_get_all_plants(limit)


@app.get(
    "/plants/{id_plant}",
    tags=["Plants"],
    responses={
        status.HTTP_200_OK: {
            "description": "Return the plant with the given ID."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The plant with the given ID was not found"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error"
        },
    },
)
async def get_one_plant(req: Request, id_plant: int):
    return plants_controller.handle_get_plant(id_plant)


@app.delete(
    "/plants/{id_plant}",
    tags=["Plants"],
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully deleted DevicePlant relation \
                    but the Plant was already deleted OR Successfully deleted \
                    Plant but the DevicePlant relations was already deleted."
        },
        status.HTTP_204_NO_CONTENT: {
            "description": "Plant and DevicePlant relation was already deleted"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error"
        },
    },
)
async def delete_plant(response: Response, id_plant: int):
    return await plants_controller.handle_delete_plant(response, id_plant)


@app.get(
    "/plant-type",
    tags=["Plant types"],
)
async def get_all_plant_types(req: Request, limit: Optional[int] = None):
    return plants_controller.handle_get_all_plant_types(limit)


@app.get(
    "/plant-type/{botanical_name}",
    tags=["Plant types"],
)
async def get_plant_type(
    botanical_name: str,
):
    return plants_controller.handle_get_plant_type(botanical_name)


@app.post(
    "/logs",
    tags=["Logs"],
)
async def create_log(
    item: LogCreateSchema
):
    return plants_controller.handle_create_log(item)


@app.get(
    "/logs/{user_id}",
)
async def get_logs_by_user(
    user_id: int,
    year: int = Query(..., gt=0),
    month: Optional[int] = Query(None, ge=1, le=12)
):
    return plants_controller.handle_get_logs_by_user(user_id, year, month)


@app.patch(
    "/{id_log}",
)
async def update_fields_in_log(id_log: str,
                               log_update_set:
                               LogPartialUpdateSchema = Body(...)):
    return plants_controller.handle_update_log(id_log, log_update_set)


@app.post(
    "/{id_log}/photos",
)
async def add_photo(id_log: str,
                    photo_create_set:
                    LogPhotoCreateSchema = Body(...)):
    return plants_controller.handle_add_photo(id_log, photo_create_set)


@app.delete(
    "/{id_log}/photos/{id_photo}",
)
async def delete_photo(id_log: int,
                       id_photo: int):
    return plants_controller.handle_delete_photo(id_log, id_photo)
