from sqlalchemy import create_engine, select, delete, engine
from sqlalchemy import update
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from os import environ
from app.database.models.Log import Log, LogPhoto
from app.database.models.base import Base
from app.database.models.plant_type import PlantType
from app.database.models.plant import Plant

from typing import List, Optional
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

    def get_plant_by_id(self, id_received: str) -> Plant:
        query = select(Plant).where(Plant.id == id_received)
        result = self.session.scalars(query).one()
        return result

    def get_all_plants(self, limit: int) -> List[Plant]:
        query = select(Plant).limit(limit)
        result = self.session.scalars(query)
        return result

    def delete_plant(self, id_received: str) -> int:
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

    def get_all_plants_by_user(self, id_user: int, limit: int) -> List[Plant]:
        query = select(Plant).where(Plant.id_user == id_user).limit(limit)
        result = self.session.scalars(query)
        return result

    def add(self, record: Base):
        self.session.add(record)
        self.session.commit()

    def get_all_plant_types(self, limit: int) -> List[PlantType]:
        query = select(PlantType).limit(limit)
        result = self.session.scalars(query)
        return result

    def get_logs_between(self,
                         user_id: int,
                         cleft: date,
                         cright: date) -> List[Log]:
        query = select(Log).\
            where(Log.created_at.between(cleft, cright)).\
            where(Log.plant.has(Plant.id_user == user_id)).\
            order_by(Log.created_at.asc())
        result = self.session.scalars(query)
        return result

    def get_plant_type_by_botanical_name(
            self, botanical_name_given: str) -> PlantType:
        query = select(PlantType).where(
            PlantType.botanical_name == botanical_name_given)
        result = self.session.scalars(query).one()
        return result

    def update_log(self,
                   log_id: str,
                   title: Optional[str],
                   content: Optional[str],
                   plant_id: Optional[int]):
        query = update(Log).where(Log.id == log_id)
        if title:
            query = query.values(title=title)
        elif content:
            query = query.values(content=content)
        elif plant_id:
            query = query.values(plant_id=plant_id)
        else:
            return False
        self.session.execute(query)
        self.session.commit()
        return True

    def find_by_log_id(self, log_id: str) -> Log:
        query = select(Log).where(Log.id == log_id)
        result = self.session.scalars(query).one()
        return result

    def delete_photo_from_log(self, id_log: int, id_photo: int) -> int:
        query = delete(LogPhoto).where(
            LogPhoto.id == id_photo and LogPhoto.log_id == id_log)
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount
