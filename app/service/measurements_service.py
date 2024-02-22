import logging
import httpx
from os import environ
from fastapi import status, HTTPException

logger = logging.getLogger("app")
logger.setLevel("DEBUG")

MEASUREMENTS_SERVICE_URL = environ["MEASUREMENTS_SERVICE_URL"]


class MeasurementService:
    @staticmethod
    async def delete(path):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(MEASUREMENTS_SERVICE_URL + path)
                return response
        except Exception as e:
            logger.error(
                "Measurements service cannot be accessed because: " + str(e)
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Measurements service cannot be accessed",
            )

    @staticmethod
    async def delete_device_plant(plant_id: str):
        return await MeasurementService.delete(
            f"/device-plant/{plant_id}?type_id=id_plant"
            )
