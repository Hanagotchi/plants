from typing import Optional, List
from app.exceptions.row_not_found import RowNotFoundError
from app.schemas.Log import (
    LogCreateSchema,
    LogPartialUpdateSchema,
    LogPhotoCreateSchema,
    LogSchema
)
from app.schemas.plant import PlantCreateSchema, PlantSchema
from app.schemas.plant_type import PlantTypeSchema
from app.service.Plants import PlantsService
from app.exceptions.internal_service_access import InternalServiceAccessError
from fastapi import HTTPException, status, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class PlantController:

    def __init__(self, plants_service: PlantsService):
        self.plants_service = plants_service

    async def handle_create_log(self,
                                input_log: LogCreateSchema,
                                token: str) -> JSONResponse:
        log: LogSchema = await self.plants_service.create_log(input_log, token)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=jsonable_encoder(log)
        )

    async def handle_get_log(self, log_id: int, token: str) -> JSONResponse:
        log: LogSchema = await self.plants_service.get_log(log_id, token)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(log)
        )

    async def handle_get_logs_by_user(
        self,
        user_id: int,
        year: int,
        month: Optional[int],
        token: str
    ) -> JSONResponse:
        log_list: List[LogSchema] = await self.plants_service.get_logs_by_user(
            user_id, year, month, token
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(log_list)
        )

    async def handle_update_log(
        self,
        log_id: str,
        log_update_set: LogPartialUpdateSchema,
        token: str
    ) -> JSONResponse:
        log: Optional[LogSchema] = await self.plants_service.update_log(
            log_id, log_update_set, token
        )

        if log:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=jsonable_encoder(log)
            )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not found a log with id {log_id}"
        )

    async def handle_add_photo(
        self,
        id_log: str,
        photo_create_set: LogPhotoCreateSchema,
        token: str
    ) -> JSONResponse:
        log: LogSchema = await self.plants_service.add_photo(
            id_log, photo_create_set, token
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=jsonable_encoder(log)
        )

    async def handle_delete_photo(
        self,
        response: Response,
        id_log: int,
        id_photo: int,
        token: str
    ) -> JSONResponse:
        try:
            await self.plants_service.delete_photo(id_log, id_photo, token)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="Photo deleted successfully"
            )
        except RowNotFoundError:
            response.status_code = status.HTTP_204_NO_CONTENT

    def handle_get_plant_type(self, botanical_name: str) -> JSONResponse:
        plant_type: PlantTypeSchema = self.plants_service.get_plant_type(
            botanical_name
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(plant_type)
        )

    def handle_get_all_plant_types(self, limit: Optional[int]) -> JSONResponse:
        plant_type_list: List[PlantTypeSchema] = self.plants_service\
            .get_all_plant_types(limit)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(plant_type_list)
        )

    async def handle_create_plant(self,
                                  data: PlantCreateSchema,
                                  token: str) -> JSONResponse:
        try:
            plant: PlantSchema = await self.plants_service.create_plant(data, token)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=jsonable_encoder(plant)
            )
        except RowNotFoundError as err:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=jsonable_encoder(err.detail)
            )
        except InternalServiceAccessError as err:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=jsonable_encoder(err.detail)
            )

    def handle_get_plant(self, id_received: int) -> JSONResponse:
        plant: PlantSchema = self.plants_service.get_plant(id_received)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(plant)
        )

    async def handle_get_plants_by_user(
            self,
            limit: int,
            token: str
            ) -> JSONResponse:
        user_plant_list: List[PlantSchema] = await self.plants_service\
                .get_plants_by_user(limit, token)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(user_plant_list)
        )

    async def handle_delete_device_plant_association(
        self, response: Response, id_plant: int, result_plant: int
    ) -> JSONResponse:
        result: str = await self.plants_service\
            .delete_device_plant_association(response, id_plant, result_plant)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result
        )

    async def handle_delete_plant(
            self,
            response: Response,
            id_plant: int,
            token: str
    ) -> JSONResponse:
        try:
            await self.plants_service.delete_plant(id_plant, token)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="Plant deleted successfully",
            )
        except RowNotFoundError:
            response.status_code = status.HTTP_204_NO_CONTENT
        except InternalServiceAccessError as err:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=jsonable_encoder(err.detail)
            )
