from fastapi import FastAPI
from app.database.database import SQLAlchemyClient
import logging
from app.router import api_router

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

app.include_router(api_router)
