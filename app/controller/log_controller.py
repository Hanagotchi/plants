from fastapi import Request
from app.database.models.Log import Log
from app.schemas.Log import (
    LogCreateSchema
)
from app.utils.sql_exception_handling import withSQLExceptionsHandle
from typing import Optional, List
from datetime import date, timedelta


@withSQLExceptionsHandle
def create_log(req: Request, input_log: LogCreateSchema) -> Log:
    try:
        log: Log = Log.from_pydantic(input_log)
        req.app.database.add(log)
        return log
    except Exception as err:
        req.app.database.rollback()
        raise err


@withSQLExceptionsHandle
def get_logs(req: Request, year: int, month: Optional[int]) -> List[Log]:
    if month:
        left = date(year, month, 1)
        right = left + timedelta(weeks=4)
    else:
        left = date(year, 1, 1)
        right = date(year+1, 1, 1)

    return req.app.database.get_logs_between(left, right)
