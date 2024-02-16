from sqlalchemy import create_engine, select, delete, engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from os import environ

from app.database.models.Log import Log, LogPhoto
from app.database.models.base import Base
from app.database.models.plant_type import PlantType
from app.database.models.plant import Plant

from typing import List
from datetime import date

load_dotenv()


class SQLAlchemyClient:
    db_url = engine.URL.create(
        "postgresql",
        database=environ["PLANTS_DB"],
        username=environ["POSTGRES_USER"],
        password=environ["POSTGRES_PASSWORD"],
        host=environ["POSTGRES_HOST"],
        port=environ["POSTGRES_PORT"],
    )

    engine = create_engine(db_url)

    def __init__(self):
        self.conn = self.engine.connect()
        self.session = Session(self.engine)

    def shutdown(self):
        self.conn.close()
        self.session.close()

    def rollback(self):
        self.session.rollback()

    def clean_table(self, table: Base):
        query = delete(table)
        self.session.execute(query)
        self.session.commit()

    def find_by_id(self, id_received: str) -> Plant:
        query = select(Plant).where(Plant.id == id_received)
        result = self.session.scalars(query).one()
        return result

    def find_all(self, limit: int) -> List[Plant]:
        query = select(Plant).limit(limit)
        result = self.session.scalars(query)
        return result

    def delete_by_id(self, id_received: str) -> int:
        """
        Delete a plant by id
        Args:
            id_received (str): id of the plant to delete
        Returns:
            int: number of rows affected. 0 if no rows were affected
        """
        query = delete(Plant).where(Plant.id == id_received)
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount

    def find_all_by_user(self, id_user: int, limit: int) -> List[Plant]:
        query = select(Plant).where(Plant.id_user == id_user).limit(limit)
        result = self.session.scalars(query)
        return result

    def add(self, record: Base):
        self.session.add(record)
        self.session.commit()

    def find_all_plant_types(self, limit: int) -> List[PlantType]:
        query = select(PlantType).limit(limit)
        result = self.session.scalars(query)
        return result

    def find_logs_between(self,
                          user_id: int,
                          cleft: date,
                          cright: date) -> List[Log]:
        # where(Log.plant.user_id == user_id).\
        query = select(Log).\
                where(Log.created_at.between(cleft, cright)).\
                where(Log.photos.any(LogPhoto.id == 3)).\
                order_by(Log.created_at.asc())
        result = self.session.scalars(query)
        return result

    def find_plant_type_by_botanical_name(
            self, botanical_name_given: str) -> PlantType:
        query = select(PlantType).where(
            PlantType.botanical_name == botanical_name_given)
        result = self.session.scalars(query).one()
        return result
