import logging
from httpx import AsyncClient, HTTPStatusError, Response
from os import environ
from fastapi import HTTPException
import json

logger = logging.getLogger("app")
logger.setLevel("DEBUG")

USERS_SERVICE_URL = environ["USERS_SERVICE_URL"]


class UserService:
    @staticmethod
    async def get(path: str) -> Response:
        try:
            async with AsyncClient() as client:
                response = await client.get(USERS_SERVICE_URL + path)
                return response.raise_for_status()
        except HTTPStatusError as e:
            logger.error("Users service cannot be accessed because: " + str(e))
            raise HTTPException(
                status_code=e.response.status_code,
                detail=json.loads(e.response.content.decode()).get(
                    "detail", "User service error"
                ),
            )

    @staticmethod
    async def get_user(user_id: int) -> Response:
        return await UserService.get(f"/users/{user_id}")
