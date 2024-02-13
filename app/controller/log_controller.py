from fastapi import Request
from app.database.models.log import Log
from app.schemas.log import (
    LogCreateSchema
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