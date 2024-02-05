from fastapi import APIRouter, Body, Request, status
from app.schemas.Log import LogSchema
from app.controller import log_controller as controller
from typing import Annotated

log = APIRouter()

create_log_examples = Body(
    openapi_examples={
        "New log": {
            "Summary": "Create log",
            "description": "A normal log when you create a new one",
            "value": {
                "title": "Mi buena petuña",
                "content": "Mi buena petuña es hermosa. Crece, crece y crece, y en verano me da mandarinas.",
                "photos":
                [
                    {
                        "photo_link": "https://pbs.twimg.com/media/EiSK6SgXsAAIQDC?format=jpg&name=small",
                    },
                    {
                        "photo_link": "https://pbs.twimg.com/media/EiSK6SgXsAAIQDC?format=jpg&name=small",
                    },
                ]
            }
        }
    }
)

@log.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=LogSchema
)
async def create_log(req: Request, item: Annotated[LogSchema, create_log_examples]):
    return controller.create_log(req, item)
