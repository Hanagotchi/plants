from fastapi import FastAPI, Request, status
from app.database.database import SQLAlchemyClient
import logging
from app.controller import plant_types_controller
from typing import List, Optional
from app.schemas.plant_type import PlantTypeSchema

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


@app.get(
    "/plant-type",
    status_code=status.HTTP_200_OK,
    response_model=List[PlantTypeSchema]
)
async def get_all_plant_types(req: Request, limit: Optional[int] = None):
    return plant_types_controller.get_all_plant_types(req, limit)


@app.get(
    "/plant-type/{botanical_name}",
    status_code=status.HTTP_200_OK,
    response_model=PlantTypeSchema
)
async def get_plant_type(
    botanical_name: str,
    req: Request,
):
    return plant_types_controller.get_plant_type(req, botanical_name)
