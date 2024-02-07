from fastapi import FastAPI, Request, status, Query
from app.database.database import SQLAlchemyClient
import logging
from app.controller import example_controller, log_controller
from typing import List
from app.schemas.example import (
    ExampleSchema,
)
from app.schemas.Log import LogCreateSchema, LogSchema

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
    "/example",
    status_code=status.HTTP_201_CREATED,
    response_model=ExampleSchema
)
async def create_example(req: Request,
                         item: ExampleSchema):
    return example_controller.create_example(req, item)


@app.get(
    "/example",
    status_code=status.HTTP_200_OK,
    response_model=List[ExampleSchema]
)
async def get_example(req: Request,
                      id_example: str = Query(None),
                      limit: int = Query(10)):
    if id_example is None:
        return example_controller.get_all_example(req, limit)
    return [example_controller.get_example(req, id_example)]


@app.post(
    "/logs",
    status_code=status.HTTP_201_CREATED,
    response_model=LogSchema
)
async def create_log(
    req: Request, item: LogCreateSchema
):
    return log_controller.create_log(req, item)
