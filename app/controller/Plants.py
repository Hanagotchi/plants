from typing import Optional, List
from app.schemas.Log import LogCreateSchema, LogPartialUpdateSchema, LogPhotoCreateSchema, LogSchema
from app.schemas.plant import PlantCreateSchema, PlantSchema
from app.schemas.plant_type import PlantTypeSchema
from app.service.Plants import PlantsService
from fastapi import HTTPException, status, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

class PlantController:

    def __init__(self, plants_service: PlantsService):
        self.plants_service = plants_service

    def handle_create_log(self, input_log: LogCreateSchema) -> JSONResponse:
        log: LogSchema = self.plants_service.create_log(input_log)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=jsonable_encoder(log)
        )
    
    def handle_get_logs_by_user(self, 
                        user_id: int,
                        year: int,
                        month: Optional[int]) -> JSONResponse:
        log_list: List[LogSchema] = self.plants_service.get_logs_by_user(user_id, year, month)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(log_list)
        )

    def handle_update_log(
        self,
        log_id: str,
        log_update_set: LogPartialUpdateSchema
    ) -> JSONResponse:
        log: Optional[LogSchema] = self.plants_service.update_log(log_id, log_update_set)
        
        if log:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=jsonable_encoder(log)
            )
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Could not found a log with id {log_id}"
        )
        

    def handle_add_photo(self,
                id_log: str,
                photo_create_set: LogPhotoCreateSchema) -> JSONResponse:
        log: LogSchema = self.plants_service.add_photo(id_log, photo_create_set)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(log)
        )
    
    def handle_delete_photo(self, id_log: int, id_photo: int) -> JSONResponse:
        self.plants_service.delete_photo(id_log, id_photo)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="Photo deleted successfully"
        )
    
    def handle_get_plant_type(self, botanical_name: str) -> JSONResponse:
        plant_type: PlantTypeSchema = self.plants_service.get_plant_type(botanical_name)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(plant_type)
        )
    
    def handle_get_all_plant_types(self, limit: int) -> JSONResponse:
        plant_type_list: List[PlantTypeSchema] = self.plants_service.get_all_plant_types(limit)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(plant_type_list)
        )
    
    def handle_create_plant(self, data: PlantCreateSchema) -> JSONResponse:
        plant: PlantSchema = self.plants_service.create_plant(data)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(plant)
        )

    def handle_get_plant(self, id_received: int) -> JSONResponse:
        plant: PlantSchema = self.plants_service.get_plant(id_received)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(plant)
        )

    
    def handle_get_all_plants(self, limit: int) -> JSONResponse:
        plant_list: List[PlantSchema] = self.plants_service.get_all_plants(limit)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(plant_list)
        )

    def handle_get_plants_by_user(self, id_user: int, limit: int) -> JSONResponse:
        user_plant_list: List[PlantSchema] = self.plants_service.get_plants_by_user(id_user, limit)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(user_plant_list)
        )
    
    async def handle_delete_device_plant_association(
        self, response: Response, id_plant: int, result_plant: int
    ) -> JSONResponse:
        result: str = await self.plants_service.delete_device_plant_association(response, id_plant, result_plant)
        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content=result
        )
    
    async def handle_delete_plant(self, response: Response, id_plant: int) -> Response:
        await self.plants_service.delete_plant(response, id_plant)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="Plant deleted successfully",
        )