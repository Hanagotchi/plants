from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from sqlalchemy import ScalarResult
from app.models.Log import Log

from app.models.plant import Plant 
from app.models.base import Base
from app.models.plant_type import PlantType

class PlantsRepository(ABC):

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def get_plant_by_id(self, id_received: int) -> Plant:
        pass

    @abstractmethod
    def get_all_plants(self, limit: int) -> ScalarResult[Plant]:
        pass

    @abstractmethod
    def delete_plant(self, id_received: int) -> int:
        pass

    @abstractmethod
    def get_all_plants_by_user(self, id_user: int, limit: int) -> ScalarResult[Plant]:
        pass

    @abstractmethod
    def add(self, record: Base):
        pass

    @abstractmethod
    def get_all_plant_types(self, limit: int) -> ScalarResult[PlantType]:
        pass

    @abstractmethod
    def get_logs_between(self,
                         user_id: int,
                         cleft: date,
                         cright: date) -> ScalarResult[Log]:
        pass

    @abstractmethod
    def get_plant_type_by_botanical_name(
            self, botanical_name_given: str) -> PlantType:
        pass

    @abstractmethod
    def update_log(self,
                   log_id: str,
                   title: Optional[str],
                   content: Optional[str],
                   plant_id: Optional[int]) -> bool:
        pass

    @abstractmethod
    def find_by_log_id(self, log_id: str) -> Log:
        pass

    @abstractmethod
    def delete_photo_from_log(self, id_log: int, id_photo: int) -> int:
        pass
