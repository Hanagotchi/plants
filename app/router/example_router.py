from typing import List

from fastapi import APIRouter, Body, Request, status, Query
from app.schemas.example import (
    ExampleSchema,
)
from app.controller import example_controller as controller

example = APIRouter()


@example.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ExampleSchema
)
async def create_example(req: Request,
                                       example: ExampleSchema = Body(...)):
    return controller.create_example(req, example)


@example.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[ExampleSchema]
)
async def get_example(req: Request,
                           id_example: str = Query(None),
                           limit: int = Query(10)):
    if id_example is None:
        return controller.get_all_example(req, limit)
    return [controller.get_example(req, id_example)]
