from fastapi import APIRouter
from app.router.example_router import example
from app.router.log_router import log

api_router = APIRouter()

api_router.include_router(example, tags=["Example"], prefix="/example")
api_router.include_router(log, tags=["Log"], prefix="/log")
