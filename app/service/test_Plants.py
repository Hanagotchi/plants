import unittest
from dotenv import load_dotenv
load_dotenv()
from unittest.mock import Mock, patch
from app.schemas.plant_type import PlantTypeSchema
from app.repository.PlantsRepository import PlantsRepository
from app.service.Plants import PlantsService


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

class TestCourses(unittest.TestCase):
    def _getMock(self, classToMock, attributes=None):
        if attributes is None:
            attributes = {}
        mock = Mock(spec=classToMock)
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
