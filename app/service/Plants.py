from datetime import date, timedelta
from re import L
from fastapi import Response, status, HTTPException
from typing import List, Optional, Sequence
from pydantic import BaseModel

from app.models import plant_type

from app.models.Log import Log, LogPhoto
from app.models.base import Base
from app.models.plant import Plant
from app.models.plant_type import PlantType
from app.repository.PlantsRepository import PlantsRepository
from app.schemas.Log import LogCreateSchema, LogPartialUpdateSchema, LogPhotoCreateSchema, LogSchema
from app.schemas.plant import PlantCreateSchema, PlantSchema
from app.schemas.plant_type import PlantTypeSchema
from app.service.Measurements import MeasurementService
from app.utils.sql_exception_handling import withSQLExceptionsHandle


class PlantsService():

    def __init__(self, plants_repository: PlantsRepository):
        self.plants_repository = plants_repository

    @withSQLExceptionsHandle
    def create_log(self, input_log: LogCreateSchema) -> LogSchema:
        try:
            log = Log.from_pydantic(input_log)
            self.plants_repository.add(log)
            created_log: Log = self.plants_repository.get_log(log.id)
            return LogSchema.model_validate(created_log.__dict__)
        except Exception as err:
            self.plants_repository.rollback()
            raise err


    @withSQLExceptionsHandle
    def get_logs_by_user(self, 
                        user_id: int,
                        year: int,
                        month: Optional[int]) -> List[LogSchema]:
        if month:
            left = date(year, month, 1)
            right = left + timedelta(weeks=4)
        else:
            left = date(year, 1, 1)
            right = date(year+1, 1, 1)

        logs: Sequence[Log] = self.plants_repository.get_logs_between(user_id, left, right)
        #TODO: Este print hace que los logs se parsen bien a LogSchemas. No quitar a
        #a menos que se encuentre una mejor solucion.
        print(logs)
        return list(map(
            lambda log: LogSchema.model_validate(log.__dict__), 
            logs
        ))


    @withSQLExceptionsHandle
    def update_log(
        self,
        log_id: str,
        log_update_set: LogPartialUpdateSchema
    ) -> Optional[LogSchema]:
        try:
            result = self.plants_repository.update_log(
                log_id,
                log_update_set.title,
                log_update_set.content,
                log_update_set.plant_id
            )
            if not result:
                return None
            log = self.plants_repository.find_by_log_id(log_id)
            #TODO: Este print hace que los logs se parsen bien a LogSchemas. No quitar a
            #a menos que se encuentre una mejor solucion.
            print(log)           
            return LogSchema.model_validate(log.__dict__)
        except Exception as err:
            self.plants_repository.rollback()
            raise err


    @withSQLExceptionsHandle
    def add_photo(self,
                id_log: str,
                photo_create_set: LogPhotoCreateSchema) -> LogSchema:
        try:
            self.plants_repository.add(LogPhoto(photo_link=photo_create_set.photo_link, log_id=id_log))
            log = self.plants_repository.find_by_log_id(id_log)
            #TODO: Este print hace que los logs se parsen bien a LogSchemas. No quitar a
            #a menos que se encuentre una mejor solucion.
            print(log)
            return LogSchema.model_validate(log.__dict__)
        except Exception as err:
            self.plants_repository.rollback()
            raise err


    @withSQLExceptionsHandle
    def delete_photo(self, id_log: int, id_photo: int):
        result_rowcount = self.plants_repository.delete_photo_from_log(id_log, id_photo)
        if result_rowcount == 0:
            raise Exception("")
        
        """ return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"deleted": "Photo deleted successfully"},
        ) """


    @withSQLExceptionsHandle
    def get_plant_type(self, botanical_name: str) -> PlantTypeSchema:
        plant_type = self.plants_repository.get_plant_type_by_botanical_name(botanical_name)
        return PlantTypeSchema.model_validate(plant_type.__dict__)


    @withSQLExceptionsHandle
    def get_all_plant_types(self, limit: Optional[int]) -> List[PlantTypeSchema]:
        plant_types = self.plants_repository.get_all_plant_types(limit)
        return list(map(
            lambda pt: PlantTypeSchema.model_validate(pt.__dict__), 
            plant_types
        ))
    

    @withSQLExceptionsHandle
    def create_plant(self, data: PlantCreateSchema) -> PlantSchema:
        try:
            plant = Plant.from_pydantic(data)
            self.plants_repository.add(plant)
            created_plant: Plant = self.plants_repository.get_plant_by_id(plant.id)
            return PlantSchema.model_validate(created_plant.__dict__)
        except Exception as err:
            self.plants_repository.rollback()
            raise err


    @withSQLExceptionsHandle
    def get_plant(self, id_received: int) -> PlantSchema:
        return PlantSchema.model_validate(
            self.plants_repository.get_plant_by_id(id_received).__dict__
        )


    @withSQLExceptionsHandle
    def get_all_plants(self, limit: int) -> List[PlantSchema]:
        return list(map(
            lambda pl: PlantSchema.model_validate(pl.__dict__), 
            self.plants_repository.get_all_plants(limit)
        ))


    @withSQLExceptionsHandle
    def get_plants_by_user(self, id_user: int, limit: int) -> List[PlantSchema]:
        return list(map(
            lambda pl: PlantSchema.model_validate(pl.__dict__), 
            self.plants_repository.get_all_plants_by_user(id_user, limit)
        ))


    #@withSQLExceptionsHandle
    async def delete_device_plant_association(
        self, response: Response, id_plant: int, result_plant: int
    ) -> str:
        result_device_plant = await MeasurementService.\
                                delete_device_plant(id_plant)
        if result_device_plant.status_code == status.HTTP_200_OK:
            if result_plant == 0:
                return ("Successfully deleted DevicePlant relation "
                        "but the Plant was already deleted")
            else:
                return "Successfully deleted Plant and DevicePlant relation"
        elif result_device_plant.status_code == status.HTTP_204_NO_CONTENT:
            if result_plant == 0:
                response.status_code = status.HTTP_204_NO_CONTENT
                return
            else:
                return ("Successfully deleted Plant but the "
                        "DevicePlant relations was already deleted")
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )


    #@withSQLExceptionsHandle
    async def delete_plant(self, response: Response, id_plant: int):
        try:
            plant_to_delete = self.get_plant(id_plant)
            result_plant = self.plants_repository.delete_plant(id_plant)
            try:
                return await self.delete_device_plant_association(
                    response, id_plant, result_plant
                )
            except Exception as err:
                """ logger.error(
                    ("Could not delete DevicePlant relation! "
                    "Rolling back plant deletion")
                ) """
                self.create_plant(plant_to_delete)
                # req.app.database.rollback() - "It's not possible because an
                # external asynchronous service
                # was called and during the await's polling another database
                # transaction could have been
                # executed over which we have no control!!"
                raise err
        except HTTPException as err:
            if err.status_code == status.HTTP_404_NOT_FOUND:
                # Prevents the deletion of a device-plant association
                # if the plant was not found!
                return await self.delete_device_plant_association(response, id_plant, 0)
            else:
                self.plants_repository.rollback()
                raise err
