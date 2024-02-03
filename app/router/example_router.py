from typing import Annotated, List

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
                         item: Annotated[
                             ExampleSchema,
                             Body(
                                 openapi_examples={
                                     "normal": {
                                         "summary": "A normal example",
                                         "description": "A **normal** example works correctly.",
                                         "value": {
                                             "id": 1,
                                             "name": "Foo",
                                             "age": 20,
                                         },
                                     },
                                     "converted": {
                                         "summary": "An example with converted data",
                                         "description": "FastAPI can convert `strings` to actual `numbers` automatically. By example, this `age` field is declared as `int` but it's received as a `string`.",
                                         "value": {
                                             "id": "2",
                                             "name": "Bar",
                                             "age": "30",
                                         },
                                     },
                                     "invalid": {
                                         "summary": "Invalid data is rejected with an error",
                                         "description": "An example with invalid data. The `age` field is a `string` but it's not a valid `number`.",
                                         "value": {
                                             "id": 3,
                                             "name": "Baz",
                                             "age": "thirty five",
                                         },
                                     },
                                     "missing": {
                                            "summary": "Missing data is rejected with an error",
                                            "description": "An example with missing data. The `age` field is missing.",
                                            "value": {
                                                "id": 4,
                                                "name": "Qux",
                                            },
                                        },
                                 },
                             ),
                         ]):
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
