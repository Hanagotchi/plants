import logging
from fastapi import HTTPException
from httpx import (
    AsyncHTTPTransport,
    AsyncClient,
    HTTPStatusError,
    Response
)
from os import environ
from app.exceptions.internal_service_access import InternalServiceAccessError
from app.exceptions.row_not_found import RowNotFoundError

logger = logging.getLogger("app")
logger.setLevel("DEBUG")

USERS_SERVICE_URL = environ["USERS_SERVICE_URL"]
NUMBER_OF_RETRIES = 3
TIMEOUT = 10


class UserService:
    @staticmethod
    async def get(path: str) -> Response:
        async with AsyncClient(
            transport=AsyncHTTPTransport(retries=NUMBER_OF_RETRIES),
            timeout=TIMEOUT
        ) as client:
            response = await client.get(USERS_SERVICE_URL + path)
            return response.raise_for_status()

    @staticmethod
    async def get_user_id(token: str) -> int:
        try:
            async with AsyncClient(
                transport=AsyncHTTPTransport(retries=NUMBER_OF_RETRIES),
                timeout=TIMEOUT
            ) as client:
                response = await client.post(
                    USERS_SERVICE_URL + "users/token", json={"token": token}
                )
                response.raise_for_status()
                user_id = response.json().get("user_id")
                return user_id

        except HTTPStatusError as e:
            logger.error("Error while getting user ID: " + str(e))
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.content.decode(),
            )

    async def check_existing_user(self, user_id: int) -> Response:
        try:
            response = await UserService.get(f"/users/{user_id}")
            if response.status_code == 200:
                return
            else:
                raise RowNotFoundError("User not found")
        except HTTPStatusError as e:
            if e.response.status_code == 404:
                raise RowNotFoundError("User not found")
            else:
                raise InternalServiceAccessError(
                    "users",
                    ("There was a problem while trying" " to access the users"),
                )
        except Exception:
            raise InternalServiceAccessError(
                "users",
                ("There was a problem while trying" " to access the users"),
            )
