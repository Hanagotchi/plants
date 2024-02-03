from fastapi import APIRouter
from app.router.example_router import example

api_router = APIRouter()

api_router.include_router(example, tags=["Example"], prefix="/example")
