from fastapi import FastAPI, Request, status, Query
from app.database.database import SQLAlchemyClient
import logging
from app.controller import plant_controller
from typing import List
from app.schemas.plant import (
    PlantSchema,
)

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
        status.HTTP_400_BAD_REQUEST:
            {"description": "Invalid request body"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def create_plant(req: Request, item: PlantSchema):
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
        status.HTTP_404_NOT_FOUND: {"description": "Plants not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR:
            {"description": "Internal server error"},
    },
)
async def get_all_plants(
    req: Request, id_user: int = Query(None), limit: int = Query(1024)
):
    if id_user is not None:
        return plant_controller.get_all_plants_of_user(req, id_user, limit)

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
        status.HTTP_500_INTERNAL_SERVER_ERROR:
            {"description": "Internal server error"},
    },
)
async def get_one_plant(req: Request, id_plant: str):
    return plant_controller.get_plant(req, id_plant)
