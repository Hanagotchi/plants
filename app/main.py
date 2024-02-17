from fastapi import FastAPI, Request, Response, status, Query
from app.database.database import SQLAlchemyClient
import logging
from app.schemas.Log import LogCreateSchema, LogSchema
from app.controller import (
    plant_controller,
    plant_types_controller,
    log_controller
)
from typing import List, Optional
from app.schemas.plant import (
    PlantSchema, PlantCreateSchema
)
from app.schemas.plant_type import PlantTypeSchema

tags_metadata = [
    {"name": "Plants", "description": "Operations with plants."},
]

app = FastAPI(
    openapi_tags=tags_metadata,
    title="Plants API",
    version="0.1.0",
    summary="Microservice for plants management",
)

logger = logging.getLogger("plants")
logger.setLevel("DEBUG")


@app.on_event("startup")
async def start_up():
    app.logger = logger

    try:
        app.database = SQLAlchemyClient()
        app.logger.info("Postgres connection established")
    except Exception as e:
        app.logger.error(e)
        app.logger.error("Could not connect to Postgres client")


@app.on_event("shutdown")
async def shutdown_db_client():
    app.database.shutdown()
    app.logger.info("Postgres shutdown succesfully")


@app.post(
    "/plants",
    status_code=status.HTTP_201_CREATED,
    response_model=PlantSchema,
    tags=["Plants"],
    responses={
        status.HTTP_200_OK: {"description": "Return the plant successfully created."},
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid request body"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def create_plant(req: Request, item: PlantCreateSchema):
    return plant_controller.create_plant(req, item)


@app.get(
    "/plants",
    status_code=status.HTTP_200_OK,
    response_model=List[PlantSchema],
    tags=["Plants"],
    responses={
        status.HTTP_200_OK: {
            "description": "Return all plants or the plants of the given user."
        },
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid query parameters"},
        status.HTTP_500_INTERNAL_SERVER_ERROR:
            {"description": "Internal server error"},
    },
)
async def get_all_plants(
    req: Request, id_user: int = Query(None), limit: int = Query(1024)
):
    if id_user is not None:
        return plant_controller.get_plants_by_user(req, id_user, limit)

    return plant_controller.get_all_plants(req, limit)


@app.get(
    "/plants/{id_plant}",
    status_code=status.HTTP_200_OK,
    response_model=PlantSchema,
    tags=["Plants"],
    responses={
        status.HTTP_200_OK: {"description": "Return the plant with the given ID."},
        status.HTTP_404_NOT_FOUND: {
            "description": "The plant with the given ID was not found"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def get_one_plant(req: Request, id_plant: str):
    return plant_controller.get_plant(req, id_plant)


@app.delete(
    "/plants/{id_plant}",
    status_code=status.HTTP_200_OK,
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
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def delete_plant(response: Response, req: Request, id_plant: str):
    return await plant_controller.delete_plant(response, req, id_plant)


@app.get(
    "/plant-type",
    tags=["Plant types"],
    status_code=status.HTTP_200_OK,
    response_model=List[PlantTypeSchema]
)
async def get_all_plant_types(req: Request, limit: Optional[int] = None):
    return plant_types_controller.get_all_plant_types(req, limit)


@app.get(
    "/plant-type/{botanical_name}",
    tags=["Plant types"],
    status_code=status.HTTP_200_OK,
    response_model=PlantTypeSchema
)
async def get_plant_type(
    botanical_name: str,
    req: Request,
):
    return plant_types_controller.get_plant_type(req, botanical_name)


@app.post(
    "/logs",
    status_code=status.HTTP_201_CREATED,
    tags=["Logs"],
    response_model=LogSchema
)
async def create_log(
    req: Request, item: LogCreateSchema
):
    return log_controller.create_log(req, item)
