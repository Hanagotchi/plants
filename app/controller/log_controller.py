from fastapi import Request, Response, status
from app.database.models.Log import Log, LogPhoto
from app.schemas.Log import (
    LogCreateSchema,
    LogPartialUpdateSchema,
    LogPhotoCreateSchema
)
from app.utils.sql_exception_handling import withSQLExceptionsHandle
from typing import Optional, List
from datetime import date, timedelta
from fastapi.responses import JSONResponse


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
def get_logs_by_user(req: Request,
                     user_id: int,
                     year: int,
                     month: Optional[int]) -> List[Log]:
    if month:
        left = date(year, month, 1)
        right = left + timedelta(weeks=4)
    else:
        left = date(year, 1, 1)
        right = date(year+1, 1, 1)

    return req.app.database.get_logs_between(user_id, left, right)


@withSQLExceptionsHandle
def update_log(
    req: Request,
    log_id: str,
    log_update_set: LogPartialUpdateSchema
):
    try:
        result = req.app.database.update_log(
            log_id,
            log_update_set.title,
            log_update_set.content,
            log_update_set.plant_id
        )
        if not result:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "No fields to update"}
            )
        return req.app.database.find_by_log_id(log_id)
    except Exception as err:
        req.app.database.rollback()
        raise err


@withSQLExceptionsHandle
def add_photo(req: Request,
              id_log: str,
              photo_create_set: LogPhotoCreateSchema) -> Log:
    try:
        req.app.database.add(
            LogPhoto(photo_link=photo_create_set.photo_link, log_id=id_log))
        log = req.app.database.find_by_log_id(id_log)
        return log
    except Exception as err:
        req.app.database.rollback()
        raise err


@withSQLExceptionsHandle
def delete_photo(req: Request, response: Response, id_log: int, id_photo: int):
    result_rowcount = req.app.database.delete_photo_from_log(id_log, id_photo)
    if result_rowcount == 0:
        response.status_code = status.HTTP_204_NO_CONTENT
        return  # EMPTY RESPONSE! RESOURCE DID NOT EXIST
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"deleted": "Photo deleted successfully"},
        )
