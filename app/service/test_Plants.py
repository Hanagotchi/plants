from dotenv import load_dotenv
load_dotenv()
from app.exceptions.internal_service_access import InternalServiceAccessError
from app.schemas.Log import (
    LogCreateSchema, 
    LogPartialUpdateSchema, 
    LogPhotoCreateSchema, 
    LogPhotoSchema, 
    LogSchema
)
import unittest
import asyncio
from app.exceptions.row_not_found import RowNotFoundError
from app.service.Measurements import MeasurementService
from app.schemas.plant import PlantCreateSchema, PlantSchema
from app.service.Users import UserService
from unittest.mock import Mock, patch, MagicMock
from app.schemas.plant_type import PlantTypeSchema
from app.repository.PlantsRepository import PlantsRepository
from app.service.Plants import PlantsService
from httpx import AsyncClient, HTTPStatusError, Response
from fastapi import status, HTTPException
from datetime import date, datetime

FAKE_PLANT_TYPE_1: PlantTypeSchema = PlantTypeSchema(
    id=1,
    botanical_name="fake_botanical_name_1",
    common_name="fake_common_name_1",
    description="fake_description_1",
    cares="fake_cares_1",
    photo_link="fake_link_1"
)

FAKE_PLANT_TYPE_2: PlantTypeSchema = PlantTypeSchema(
    id=2,
    botanical_name="fake_botanical_name_2",
    common_name="fake_common_name_2",
    description="fake_description_2",
    cares="fake_cares_2",
    photo_link="fake_link_2"
)

FAKE_PLANT_1: PlantSchema = PlantSchema(
    id=1,
    id_user=1,
    name="fake_plant_1",
    scientific_name=FAKE_PLANT_TYPE_1.botanical_name
)

FAKE_PLANT_2: PlantSchema = PlantSchema(
    id=2,
    id_user=1,
    name="fake_plant_2",
    scientific_name=FAKE_PLANT_TYPE_2.botanical_name,
)

FAKE_LOG_1: LogSchema = LogSchema(
    id=1,
    title="fake_title_1",
    content="fake_content_1",
    photos=[],
    plant_id=FAKE_PLANT_1.id,
    created_at=datetime(1997, 11, 14),
    updated_at=datetime(1997, 11, 14)
)

FAKE_LOG_CREATE_SET_1: LogCreateSchema = LogCreateSchema(
    title=FAKE_LOG_1.title,
    content=FAKE_LOG_1.content,
    photos=FAKE_LOG_1.photos,
    plant_id=FAKE_LOG_1.plant_id,
)

FAKE_LOG_UPDATE_SET_1: LogPartialUpdateSchema = LogPartialUpdateSchema(
    title="new_fake_title_1",
)

FAKE_LOG_2: LogSchema = LogSchema(
    id=2,
    title="fake_title_2",
    content="fake_content_2",
    photos=[],
    plant_id=FAKE_PLANT_2.id,
    created_at=datetime(1997, 11, 14),
    updated_at=datetime(1997, 11, 14)
)

FAKE_LOG_CREATE_SET_2: LogCreateSchema = LogCreateSchema(
    title=FAKE_LOG_2.title,
    content=FAKE_LOG_2.content,
    photos=FAKE_LOG_2.photos,
    plant_id=FAKE_LOG_2.plant_id,
)

FAKE_LOG_PHOTO_CREATE_SET_1: LogPhotoCreateSchema = LogPhotoCreateSchema(
    photo_link="fake_photo_link_1"
)

FAKE_LOG_PHOTO_1: LogPhotoSchema = LogPhotoSchema(
    id=1,
    log_id=FAKE_LOG_1.id,
    photo_link=FAKE_LOG_PHOTO_CREATE_SET_1.photo_link
)

class TestCourses(unittest.IsolatedAsyncioTestCase):

    def _getMock(self, classToMock, attributes=None):
        if attributes is None:
            attributes = {}
        mock = MagicMock(spec=classToMock)
        mock.configure_mock(**attributes)
        return mock
    
    def testGetPlantTypeWorksCorrectly(self):
        attr_db = {"get_plant_type_by_botanical_name.return_value": FAKE_PLANT_TYPE_1}
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        self.assertEqual(
            service.get_plant_type("fake_botanical_name_1"), FAKE_PLANT_TYPE_1
        )
        mock_db.get_plant_type_by_botanical_name.assert_called_once_with("fake_botanical_name_1")
    
    def testGetAllPlantTypesWorksCorrectly(self):
        attr_db = {"get_all_plant_types.return_value": [FAKE_PLANT_TYPE_1, FAKE_PLANT_TYPE_2]}
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        self.assertEqual(
            service.get_all_plant_types(2), [FAKE_PLANT_TYPE_1, FAKE_PLANT_TYPE_2]
        )
        mock_db.get_all_plant_types.assert_called_once_with(2)

    def testGetPlantWorksCorrectly(self):
        attr_db = {"get_plant_by_id.return_value": FAKE_PLANT_1}
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        self.assertEqual(
            service.get_plant(1), FAKE_PLANT_1
        )
        mock_db.get_plant_by_id.assert_called_once_with(1)

    def testGetAllPlantsWorksCorrectly(self):
        attr_db = {"get_all_plants.return_value": [FAKE_PLANT_1, FAKE_PLANT_2]}
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        self.assertEqual(
            service.get_all_plants(10), [FAKE_PLANT_1, FAKE_PLANT_2]
        )
        mock_db.get_all_plants.assert_called_once_with(10)

    def testGetPlantsByUserWorksCorrectly(self):
        attr_db = {"get_all_plants_by_user.return_value": [FAKE_PLANT_1, FAKE_PLANT_2]}
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        self.assertEqual(
            service.get_plants_by_user(1, 10), [FAKE_PLANT_1, FAKE_PLANT_2]
        )
        mock_db.get_all_plants_by_user.assert_called_once_with(1, 10)

    async def testCreatePlantWorksCorrectly(self):
        plant_data = PlantCreateSchema(
            id_user=FAKE_PLANT_1.id_user,
            name=FAKE_PLANT_1.name,
            scientific_name=FAKE_PLANT_1.scientific_name
        )
        attr_db = {
            "add.return_value": None, 
            "get_plant_by_id.return_value": FAKE_PLANT_1,
            "rollback.return_value": None
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        attr_user = {"check_existing_user.return_value": Response(status_code=200)}
        mock_user = self._getMock(UserService, attr_user)
        service = PlantsService(mock_db, Mock(), mock_user)

        result = await service.create_plant(plant_data)

        self.assertEqual(result.id_user, plant_data.id_user)
        self.assertEqual(result.name, plant_data.name)
        self.assertEqual(result.scientific_name, plant_data.scientific_name)
        mock_db.rollback.assert_not_called()
        mock_user.check_existing_user.assert_called_once_with(plant_data.id_user)

    async def testCreatePlantRaiseRowNotFoundWhenThereIsNoUser(self):
        plant_data = PlantCreateSchema(
            id_user=3,
            name=FAKE_PLANT_1.name,
            scientific_name=FAKE_PLANT_1.scientific_name
        )
        attr_db = {
            "add.return_value": None, 
            "get_plant_by_id.return_value": FAKE_PLANT_1,
            "rollback.return_value": None
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        attr_user = {"check_existing_user.side_effect": RowNotFoundError(detail="fake_details")}
        mock_user = self._getMock(UserService, attr_user)
        service = PlantsService(mock_db, Mock(), mock_user)

        with self.assertRaises(RowNotFoundError):
            await service.create_plant(plant_data)

        mock_db.add.assert_not_called()
        mock_db.rollback.assert_not_called()
        mock_user.check_existing_user.assert_called_once_with(plant_data.id_user)

    async def testCreatePlantRaiseExceptionAndRollback(self):
        plant_data = PlantCreateSchema(
            id_user=3,
            name=FAKE_PLANT_1.name,
            scientific_name=FAKE_PLANT_1.scientific_name
        )
        attr_db = {
            "add.side_effect": Exception(), 
            "get_plant_by_id.return_value": FAKE_PLANT_1,
            "rollback.return_value": None
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        attr_user = {"check_existing_user.return_value": Response(status_code=200)}
        mock_user = self._getMock(UserService, attr_user)
        service = PlantsService(mock_db, Mock(), mock_user)

        with self.assertRaises(Exception):
            await service.create_plant(plant_data)

        mock_db.add.assert_called_once()
        mock_db.rollback.assert_called_once()
        mock_db.get_plant_by_id.assert_not_called()
        mock_user.check_existing_user.assert_called_once_with(plant_data.id_user)

    async def testDeletePlantWorksCorrectly(self):
        attr_db = {
            "delete_plant.delete_plant": 1,
            "rollback.return_value": None
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        attr_measurements = {"delete_device_plant.return_value": Response(status_code=200)}
        mock_measurements = self._getMock(MeasurementService, attr_measurements)
        service = PlantsService(mock_db, mock_measurements, Mock())

        await service.delete_plant(FAKE_PLANT_TYPE_1.id)

        mock_db.delete_plant.assert_called_once_with(FAKE_PLANT_TYPE_1.id)
        mock_db.rollback.assert_not_called()
        mock_measurements.delete_device_plant.assert_called_once_with(FAKE_PLANT_TYPE_1.id)

    async def testDeletePlantRaiseExceptionAndRollback(self):
        attr_db = {
            "delete_plant.side_effect": Exception(),
            "rollback.return_value": None
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        attr_measurements = {"delete_device_plant.return_value": Response(status_code=200)}
        mock_measurements = self._getMock(MeasurementService, attr_measurements)
        service = PlantsService(mock_db, mock_measurements, Mock())

        with self.assertRaises(Exception):
            await service.delete_plant(FAKE_PLANT_TYPE_1.id)

        mock_db.delete_plant.assert_called_once_with(FAKE_PLANT_TYPE_1.id)
        mock_db.rollback.assert_called_once()
        mock_measurements.delete_device_plant.assert_not_called()

    async def testDeletePlantRaiseRowNotFoundErrorAndRollback(self):
        attr_db = {
            "delete_plant.return_value": 0,
            "rollback.return_value": None
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        attr_measurements = {"delete_device_plant.return_value": Response(status_code=200)}
        mock_measurements = self._getMock(MeasurementService, attr_measurements)
        service = PlantsService(mock_db, mock_measurements, Mock())

        with self.assertRaises(RowNotFoundError):
            await service.delete_plant(FAKE_PLANT_TYPE_1.id)

        mock_db.delete_plant.assert_called_once_with(FAKE_PLANT_TYPE_1.id)
        mock_db.rollback.assert_called_once()
        mock_measurements.delete_device_plant.assert_not_called()

    async def testDeletePlantWorksCorrectlyWhenMeasurementServiceThrowHttpExceptionWithStatusCode404(self):
        attr_db = {
            "delete_plant.return_value": 1,
            "rollback.return_value": None
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        attr_measurements = {"delete_device_plant.side_effect": HTTPException(status_code=404)}
        mock_measurements = self._getMock(MeasurementService, attr_measurements)
        service = PlantsService(mock_db, mock_measurements, Mock())

        await service.delete_plant(FAKE_PLANT_TYPE_1.id)

        mock_db.delete_plant.assert_called_once_with(FAKE_PLANT_TYPE_1.id)
        mock_db.rollback.assert_not_called()
        mock_measurements.delete_device_plant.assert_called_once_with(FAKE_PLANT_TYPE_1.id)

    async def testDeletePlantThrowInternalServiceAccessError(self):
        attr_db = {
            "delete_plant.return_value": 1,
            "rollback.return_value": None
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        attr_measurements = {"delete_device_plant.side_effect": HTTPException(status_code=500)}
        mock_measurements = self._getMock(MeasurementService, attr_measurements)
        service = PlantsService(mock_db, mock_measurements, Mock())

        with self.assertRaises(InternalServiceAccessError):
            await service.delete_plant(FAKE_PLANT_TYPE_1.id)

        mock_db.delete_plant.assert_called_once_with(FAKE_PLANT_TYPE_1.id)
        mock_db.rollback.assert_not_called()
        mock_measurements.delete_device_plant.assert_called_once_with(FAKE_PLANT_TYPE_1.id)

    def testGetLogWorksCorrectly(self):
        attr_db = {
            "get_log.return_value": FAKE_LOG_1,
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        self.assertEqual(
            service.get_log(FAKE_LOG_1.id), FAKE_LOG_1
        )
        mock_db.get_log.assert_called_once_with(FAKE_LOG_1.id)

    def testGetLogsByUserWorksCorrectlyWithMonth(self):
        FAKE_USER_ID = 1
        attr_db = {
            "get_logs_between.return_value": [FAKE_LOG_1, FAKE_LOG_2],
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        self.assertEqual(
            service.get_logs_by_user(FAKE_USER_ID, 2024, 3), [FAKE_LOG_1, FAKE_LOG_2]
        )
        mock_db.get_logs_between.assert_called_once_with(FAKE_USER_ID, date(2024, 3, 1), date(2024, 4, 1))

    def testGetLogsByUserWorksCorrectlyWithDecemberAsMonth(self):
        FAKE_USER_ID = 1
        attr_db = {
            "get_logs_between.return_value": [FAKE_LOG_1, FAKE_LOG_2],
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        self.assertEqual(
            service.get_logs_by_user(FAKE_USER_ID, 2024, 12), [FAKE_LOG_1, FAKE_LOG_2]
        )
        mock_db.get_logs_between.assert_called_once_with(FAKE_USER_ID, date(2024, 12, 1), date(2025, 1, 1))

    def testGetLogsByUserWorksCorrectlyWithoutMonth(self):
        FAKE_USER_ID = 1
        attr_db = {
            "get_logs_between.return_value": [FAKE_LOG_1, FAKE_LOG_2],
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        self.assertEqual(
            service.get_logs_by_user(FAKE_USER_ID, 2024, None), [FAKE_LOG_1, FAKE_LOG_2]
        )
        mock_db.get_logs_between.assert_called_once_with(FAKE_USER_ID, date(2024, 1, 1), date(2025, 1, 1))

    def testCreateLogWorksCorrectly(self):
        attr_db = {
            "add.return_value": None,
            "get_log.return_value": FAKE_LOG_1,
            "rollback.return_value": None,
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        self.assertEqual(
            service.create_log(FAKE_LOG_CREATE_SET_1), FAKE_LOG_1
        )
        mock_db.add.assert_called_once()
        mock_db.get_log.assert_called_once()
        mock_db.rollback.assert_not_called()

    def testCreateLogWorksThrowsExceptionAndRollback(self):
        attr_db = {
            "add.side_effect": Exception(),
            "get_log.return_value": FAKE_LOG_1,
            "rollback.return_value": None,
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        with self.assertRaises(Exception):
            service.create_log(FAKE_LOG_CREATE_SET_1)

        mock_db.add.assert_called_once()
        mock_db.get_log.assert_not_called()
        mock_db.rollback.assert_called_once()

    def testUpdateLogWorksCorrectly(self):
        attr_db = {
            "update_log.return_value": True,
            "find_by_log_id.return_value": FAKE_LOG_1,
            "rollback.return_value": None,
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        self.assertEqual(
            service.update_log(str(FAKE_LOG_1.id), FAKE_LOG_UPDATE_SET_1), FAKE_LOG_1
        )
        mock_db.update_log.assert_called_once()
        mock_db.find_by_log_id.assert_called_once()
        mock_db.rollback.assert_not_called()

    def testUpdateLogThrowsExceptionAndRollback(self):
        attr_db = {
            "update_log.side_effect": Exception(),
            "find_by_log_id.return_value": FAKE_LOG_1,
            "rollback.return_value": None,
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        with self.assertRaises(Exception):
            service.update_log(str(FAKE_LOG_1.id), FAKE_LOG_UPDATE_SET_1)

        mock_db.update_log.assert_called_once()
        mock_db.find_by_log_id.assert_not_called()
        mock_db.rollback.assert_called_once()
        
    def testAddLogPhotoWorksCorrectly(self):
        attr_db = {
            "add.return_value": None,
            "find_by_log_id.return_value": FAKE_LOG_1,
            "rollback.return_value": None,
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        self.assertEqual(
            service.add_photo(str(FAKE_LOG_1.id), FAKE_LOG_PHOTO_CREATE_SET_1), FAKE_LOG_1
        )
        mock_db.add.assert_called_once()
        mock_db.find_by_log_id.assert_called_once_with(str(FAKE_LOG_1.id))
        mock_db.rollback.assert_not_called()

    def testAddLogPhotoThrowsExceptionAndRollback(self):
        attr_db = {
            "add.side_effect": Exception(),
            "find_by_log_id.return_value": FAKE_LOG_1,
            "rollback.return_value": None,
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        with self.assertRaises(Exception):
            service.add_photo(str(FAKE_LOG_1.id), FAKE_LOG_PHOTO_CREATE_SET_1)

        mock_db.add.assert_called_once()
        mock_db.find_by_log_id.assert_not_called()
        mock_db.rollback.assert_called_once()

    def testDeleteLogPhotoWorksCorrectly(self):
        attr_db = {
            "delete_photo_from_log.return_value": 1,
            "rollback.return_value": None,
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        service.delete_photo(FAKE_LOG_1.id, FAKE_LOG_PHOTO_1.id)
        
        mock_db.delete_photo_from_log.assert_called_once_with(FAKE_LOG_1.id, FAKE_LOG_PHOTO_1.id)
        mock_db.rollback.assert_not_called()

    def testDeleteLogPhotoThrowsNotRowFoundErrorAndRollback(self):
        attr_db = {
            "delete_photo_from_log.return_value": 0,
            "rollback.return_value": None,
        }
        mock_db = self._getMock(PlantsRepository, attr_db)
        service = PlantsService(mock_db, Mock(), Mock())

        with self.assertRaises(RowNotFoundError):
            service.delete_photo(FAKE_LOG_1.id, FAKE_LOG_PHOTO_1.id)
        
        mock_db.delete_photo_from_log.assert_called_once_with(FAKE_LOG_1.id, FAKE_LOG_PHOTO_1.id)
        mock_db.rollback.assert_called_once()