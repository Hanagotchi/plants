from fastapi import Request
from app.database.models.Log import Log
from app.schemas.Log import (
    LogSchema, LogCreateSchema
)
from app.utils.sql_exception_handling import withSQLExceptionsHandle


@withSQLExceptionsHandle
def create_log(req: Request, input_log: LogCreateSchema):
    try:
        log: Log = Log.from_pydantic(input_log)
        req.app.database.add(log)
        return log
    except Exception as err:
        req.app.database.rollback()
        raise err
