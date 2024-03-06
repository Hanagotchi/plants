from typing import Optional, List
from app.schemas.Log import LogCreateSchema, LogPartialUpdateSchema, LogPhotoCreateSchema
from app.schemas.plant import PlantCreateSchema, PlantSchema
from app.service.Plants import PlantsService
from fastapi import HTTPException, status, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

class PlantController:

    def __init__(self, plants_service: PlantsService):
        self.plants_service = plants_service

    def handle_create_log(self, input_log: LogCreateSchema) -> Response:
        log = self.plants_service.create_log(input_log)
        return Response(status_code=status.HTTP_201_CREATED, content=log)
    
    def handle_get_logs_by_user(self, 
                        user_id: int,
                        year: int,
                        month: Optional[int]) -> Response:
        log_list = self.plants_service.get_logs_by_user
        return Response(status_code=status.HTTP_200_OK, content=log_list)

    def handle_update_log(
        self,
        log_id: str,
        log_update_set: LogPartialUpdateSchema
    ) -> Response:
        log = self.plants_service.update_log(log_id, log_update_set)
        if log:
            return Response(status_code=status.HTTP_200_OK, content=log)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        

    def handle_add_photo(self,
                id_log: str,
                photo_create_set: LogPhotoCreateSchema) -> Response:
        log = self.plants_service.add_photo(id_log, photo_create_set)
        return Response(status_code=status.HTTP_200_OK, content=log)
    
    def handle_delete_photo(self, id_log: int, id_photo: int) -> Response:
        self.plants_service.delete_photo(id_log, id_photo)
        return Response(status_code=status.HTTP_200_OK)
    
    def handle_get_plant_type(self, botanical_name: str) -> Response:
        plant_type = self.plants_service.get_plant_type(botanical_name)
        return Response(status_code=status.HTTP_200_OK, content=plant_type)
    
    def handle_get_all_plant_types(self, limit: int) -> Response:
        plant_type_list = self.plants_service.get_all_plant_types(limit)
        return Response(status_code=status.HTTP_200_OK, content=plant_type_list)
    
    def handle_create_plant(self, data: PlantCreateSchema) -> PlantSchema:
        return self.plants_service.create_plant(data)

    def handle_get_plant(self, id_received: int) -> JSONResponse:
        plant = self.plants_service.get_plant(id_received)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(plant)
        )

    
    def handle_get_all_plants(self, limit: int) -> JSONResponse:
        plant_list = self.plants_service.get_all_plants(limit)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(plant_list)
        )

    def handle_get_plants_by_user(self, id_user: int, limit: int) -> JSONResponse:
        user_plant_list = self.plants_service.get_plants_by_user(id_user, limit)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(user_plant_list)
        )
    
    async def handle_delete_device_plant_association(
        self, response: Response, id_plant: int, result_plant: int
    ) -> Response:
        result = await self.plants_service.delete_device_plant_association(response, id_plant, result_plant)
        return Response(status_code=status.HTTP_200_OK, content=result)
    
    async def handle_delete_plant(self, response: Response, id_plant: int) -> Response:
        await self.plants_service.delete_plant(response, id_plant)
        return Response(status_code=status.HTTP_200_OK)