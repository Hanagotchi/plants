from fastapi import FastAPI, Request, status, Query
from app.database.database import SQLAlchemyClient
import logging
from app.controller import plant_controller
from typing import List
from app.schemas.plant import (
    PlantSchema,
)

app = FastAPI()

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post(
    "/plants",
    status_code=status.HTTP_201_CREATED,
    response_model=PlantSchema
)
async def create_plant(req: Request,
                         item: PlantSchema):
    return plant_controller.create_plant(req, item)


@app.get(
    "/plants",
    status_code=status.HTTP_200_OK,
    response_model=List[PlantSchema]
)
async def get_all_plants(req: Request,
                      id_user: int = Query(None),
                      limit: int = Query(1024)):
    if id_user is not None:
        return plant_controller.get_all_plants_of_user(req, id_user, limit)
            
    return plant_controller.get_all_plants(req, limit)


@app.get(
    "/plants/{id_plant}",
    status_code=status.HTTP_200_OK,
    response_model=PlantSchema
)
async def get_one_plant(req: Request, id_plant: str):
    return plant_controller.get_plant(req, id_plant)