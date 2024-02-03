from typing import Union
from fastapi import Request, status, HTTPException
from app.database.models.example import Example
from app.schemas.example import (
    ExampleSchema,
)
import logging
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import PendingRollbackError, IntegrityError, NoResultFound

logger = logging.getLogger("app")
logger.setLevel("DEBUG")


def withSQLExceptionsHandle(func):
    def handleSQLException(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                parsed_error = err.orig.pgerror.split("\n")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error": parsed_error[0],
                        "detail": parsed_error[1]
                    })

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=format(err))

        except PendingRollbackError as err:
            logger.warning(format(err))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=format(err))

        except NoResultFound as err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=format(err))

    return handleSQLException


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
