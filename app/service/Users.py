import logging
from httpx import AsyncClient, HTTPStatusError, Response
from os import environ
from app.exceptions.internal_service_access import InternalServiceAccessError
from app.exceptions.row_not_found import RowNotFoundError

logger = logging.getLogger("app")
logger.setLevel("DEBUG")

USERS_SERVICE_URL = environ["USERS_SERVICE_URL"]


class UserService:
    @staticmethod
    async def get(path: str) -> Response:
        async with AsyncClient() as client:
            response = await client.get(USERS_SERVICE_URL + path)
            return response.raise_for_status()

    @staticmethod
    async def check_existing_user(user_id: int) -> Response:
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
