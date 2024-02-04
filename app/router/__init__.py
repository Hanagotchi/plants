from fastapi import APIRouter
from app.router.example_router import example
from app.router.plant_types_router import plant_type

api_router = APIRouter()

api_router.include_router(example, tags=["Example"], prefix="/example")
api_router.include_router(plant_type, tags=["PlantType"], prefix="/plant-type")
