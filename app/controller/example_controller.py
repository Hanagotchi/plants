from fastapi import Request
from app.database.models.example import Example
from app.schemas.example import (
    ExampleSchema,
)


from app.utils.sql_exception_handling import withSQLExceptionsHandle


@withSQLExceptionsHandle
def create_example(req: Request, example: ExampleSchema):
    try:
        req.app.database.add(Example.from_pydantic(example))
        return req.app.database.find_by_id(example.id)
    except Exception as err:
        req.app.database.rollback()
        raise err


@withSQLExceptionsHandle
def get_example(req: Request, id_received: str):
    return req.app.database.find_by_id(id_received)


@withSQLExceptionsHandle
def get_all_example(req: Request, limit: int):
    return req.app.database.find_all(limit)
