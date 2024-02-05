from fastapi import APIRouter, Request, status
from app.schemas.Log import LogSchema
from app.controller import log_controller as controller

log = APIRouter()


@log.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=LogSchema
)
async def create_example(req: Request, item: LogSchema):
    return controller.create_log(req, item)
