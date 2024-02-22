from fastapi import Request
from app.utils.sql_exception_handling import withSQLExceptionsHandle


@withSQLExceptionsHandle
def get_plant_type(req: Request, botanical_name: str):
    return req.app.database.get_plant_type_by_botanical_name(botanical_name)


@withSQLExceptionsHandle
def get_all_plant_types(req: Request, limit: int):
    return req.app.database.get_all_plant_types(limit)
