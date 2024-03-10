import logging
from httpx import AsyncClient, HTTPStatusError, Response
from os import environ
from fastapi import HTTPException

logger = logging.getLogger("app")
logger.setLevel("DEBUG")

MEASUREMENTS_SERVICE_URL = environ["MEASUREMENTS_SERVICE_URL"]


class MeasurementService:
    @staticmethod
    async def delete(path: str) -> Response:
        try:
            async with AsyncClient() as client:
                response = await client.delete(MEASUREMENTS_SERVICE_URL + path)
                return response.raise_for_status()
        except HTTPStatusError as e:
            logger.error(
                "Measurements service cannot be accessed because: " + str(e)
            )
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.content,
            )

    @staticmethod
    async def delete_device_plant(plant_id: int) -> Response:
        return await MeasurementService.delete(
            f"/device-plant/{plant_id}?type_id=id_plant"
        )
