from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import PendingRollbackError, IntegrityError, NoResultFound
from fastapi import status, HTTPException
import logging

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
