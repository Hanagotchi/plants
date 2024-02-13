from fastapi import Request, Response, status, HTTPException
from app.database.models.plant import Plant
from app.schemas.plant import (
    PlantSchema,
)
import logging
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import (
    PendingRollbackError,
    DataError,
    IntegrityError,
    NoResultFound,
    InternalError,
)

from app.service.measurements_service import MeasurementService

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
                    detail={"error": parsed_error[0], "detail": parsed_error[1]},
                )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=format(err)
            )

        except (PendingRollbackError, InternalError, DataError) as err:
            logger.warning(format(err))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=format(err)
            )

        except NoResultFound as err:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=format(err)
            )

    return handleSQLException


@withSQLExceptionsHandle
def create_plant(req: Request, example: PlantSchema):
    try:
        req.app.database.add(Plant.from_pydantic(example))
        return req.app.database.find_by_id(example.id)
    except Exception as err:
        req.app.database.rollback()
        raise err


@withSQLExceptionsHandle
def get_plant(req: Request, id_received: str):
    return req.app.database.find_by_id(id_received)


@withSQLExceptionsHandle
def get_all_plants(req: Request, limit: int):
    return req.app.database.find_all(limit)


@withSQLExceptionsHandle
def get_plants_by_user(req: Request, id_user: int, limit: int):
    return req.app.database.find_all_by_user(id_user, limit)


@withSQLExceptionsHandle
async def delete_device_plant_association(
    response: Response, id_plant: str, result_plant: int
) -> str:
    result_device_plant = await MeasurementService.delete_device_plant(id_plant)
    if result_device_plant.status_code == status.HTTP_200_OK:
        if result_plant == 0:
            return "Successfully deleted DevicePlant relation but the Plant was already deleted"
        else:
            return "Successfully deleted Plant and DevicePlant relation"
    elif result_device_plant.status_code == status.HTTP_204_NO_CONTENT:
        if result_plant == 0:
            response.status_code = status.HTTP_204_NO_CONTENT
            return
        else:
            return "Successfully deleted Plant but the DevicePlant relations was already deleted"
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


async def delete_plant(response: Response, req: Request, id_plant: str):
    try:
        plant_to_delete = get_plant(req, id_plant)
        result_plant = req.app.database.delete_by_id(id_plant)
        try:
            return await delete_device_plant_association(
                response, id_plant, result_plant
            )
        except Exception as err:
            logger.error(
                "Could not delete DevicePlant relation! Rolling back plant deletion"
            )
            create_plant(req, plant_to_delete)
            # req.app.database.rollback() - "It's not possible because an external asynchronous service
            # was called and during the await's polling another database transaction could have been
            # executed over which we have no control!!"
            raise err
    except HTTPException as err:
        if err.status_code == status.HTTP_404_NOT_FOUND:
            # Prevents the deletion of a device-plant association if the plant was not found!
            return await delete_device_plant_association(response, id_plant, 0)
        else:
            req.app.database.rollback()
            raise err
