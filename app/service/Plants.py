from datetime import date
import logging
from fastapi import status, HTTPException
from typing import List, Optional, Sequence
from app.exceptions.internal_service_access import InternalServiceAccessError
from app.exceptions.row_not_found import RowNotFoundError

from app.models.plant import Plant
from app.models.Log import Log, LogPhoto
from app.repository.PlantsRepository import PlantsRepository
from app.schemas.Log import (
    LogCreateSchema,
    LogPartialUpdateSchema,
    LogPhotoCreateSchema,
    LogSchema
)
from app.schemas.plant import PlantCreateSchema, PlantSchema
from app.schemas.plant_type import PlantTypeSchema
from app.service.Measurements import MeasurementService
from app.utils.sql_exception_handling import withSQLExceptionsHandle
from app.service.Users import UserService
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

logger = logging.getLogger("app")
logger.setLevel("DEBUG")


class PlantsService():

    def __init__(self, plants_repository: PlantsRepository):
        self.plants_repository = plants_repository

    @withSQLExceptionsHandle
    def create_log(self, input_log: LogCreateSchema) -> LogSchema:
        try:
            log = Log.from_pydantic(input_log)
            self.plants_repository.add(log)
            created_log: Log = self.plants_repository.get_log(log.id)
            # TODO: Este print hace que los logs se parsen bien a LogSchemas.
            # No quitar a menos que se encuentre una mejor solucion.
            print(created_log)
            return LogSchema.model_validate(created_log.__dict__)
        except Exception as err:
            self.plants_repository.rollback()
            raise err

    @withSQLExceptionsHandle
    def get_log(self, log_id: int) -> LogSchema:
        try:
            log: Log = self.plants_repository.get_log(log_id)
            # TODO: Este print hace que los logs se parsen bien a LogSchemas.
            # No quitar a menos que se encuentre una mejor solucion.
            print(log)
            return LogSchema.model_validate(log.__dict__)
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not found a log with id {log_id}"
            )

    @withSQLExceptionsHandle
    def get_logs_by_user(
        self,
        user_id: int,
        year: int,
        month: Optional[int]
    ) -> List[LogSchema]:
        if month:
            left = date(year, month, 1)
            right = date(year+1, 1, 1) if month == 12 else date(year, month+1, 1)
        else:
            left = date(year, 1, 1)
            right = date(year+1, 1, 1)

        logs: Sequence[Log] = self.plants_repository.get_logs_between(
            user_id, left, right
        )
        # TODO: Este print hace que los logs se parsen bien a LogSchemas.
        # No quitar a menos que se encuentre una mejor solucion.
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

            log = self.plants_repository.find_by_log_id(log_id)
            # TODO: Este print hace que los logs se parsen bien a LogSchemas.
            # No quitar a menos que se encuentre una mejor solucion.
            print(log)
            return LogSchema.model_validate(log.__dict__)
        except Exception as err:
            self.plants_repository.rollback()
            raise err

    @withSQLExceptionsHandle
    def add_photo(
        self,
        id_log: str,
        photo_create_set: LogPhotoCreateSchema
    ) -> LogSchema:
        try:
            self.plants_repository.add(
                LogPhoto(photo_link=photo_create_set.photo_link, log_id=id_log)
            )
            log = self.plants_repository.find_by_log_id(id_log)
            # TODO: Este print hace que los logs se parsen bien a LogSchemas.
            # No quitar a menos que se encuentre una mejor solucion.
            print(log)
            return LogSchema.model_validate(log.__dict__)
        except Exception as err:
            self.plants_repository.rollback()
            raise err

    @withSQLExceptionsHandle
    def delete_photo(self, id_log: int, id_photo: int):
        try:
            result_rowcount = self.plants_repository.delete_photo_from_log(
                id_log, id_photo
            )
            if result_rowcount == 0:
                raise RowNotFoundError(
                    (
                        f"Could not found photo with id "
                        f"{id_photo} in log with id {id_log}"
                    )
                )
        except SQLAlchemyError as err:
            self.plants_repository.rollback()
            raise err

    @withSQLExceptionsHandle
    def get_plant_type(self, botanical_name: str) -> PlantTypeSchema:
        plant_type = self.plants_repository.\
            get_plant_type_by_botanical_name(botanical_name)
        return PlantTypeSchema.model_validate(plant_type.__dict__)

    @withSQLExceptionsHandle
    def get_all_plant_types(
        self, limit: Optional[int]
    ) -> List[PlantTypeSchema]:
        plant_types = self.plants_repository.get_all_plant_types(limit)
        return list(map(
            lambda pt: PlantTypeSchema.model_validate(pt.__dict__),
            plant_types
        ))

    @withSQLExceptionsHandle
    async def create_plant(self, data: PlantCreateSchema) -> PlantSchema:
        await UserService.check_existing_user(data.id_user)
        try:
            plant = Plant.from_pydantic(data)
            self.plants_repository.add(plant)
            created_plant: Plant = self.plants_repository.\
                get_plant_by_id(plant.id)
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
    def get_plants_by_user(
        self, id_user: int, limit: int
    ) -> List[PlantSchema]:
        return list(map(
            lambda pl: PlantSchema.model_validate(pl.__dict__),
            self.plants_repository.get_all_plants_by_user(id_user, limit)
        ))

    async def delete_plant(self, id_plant: int):
        try:
            row_count = self.plants_repository.delete_plant(id_plant)
            if row_count == 0:
                raise RowNotFoundError(
                    f"Could not found plant with id {id_plant}"
                )
        except SQLAlchemyError as err:
            self.plants_repository.rollback()
            raise err

        try:
            await MeasurementService.delete_device_plant(id_plant)
        except HTTPException as err:
            # If there is no row, ignore. It could happen sometimes :D
            if err.status_code != status.HTTP_404_NOT_FOUND:
                raise InternalServiceAccessError(
                    "measurements",
                    (
                        "There was a problem while deleting "
                        "a device_plant relation"
                    )
                )
