from sqlalchemy import create_engine, select, delete, engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from os import environ

<<<<<<< HEAD
from app.database.models.example import Example
from app.database.models.base import Base
=======
from app.database.models.base import Base
from app.database.models.PlantType import PlantType
>>>>>>> main
from typing import List

load_dotenv()


class SQLAlchemyClient():
    db_url = engine.URL.create(
        "postgresql",
        database=environ["POSTGRES_DB"],
        username=environ["POSTGRES_USER"],
        password=environ["POSTGRES_PASSWORD"],
        host=environ["POSTGRES_HOST"],
        port=environ["POSTGRES_PORT"]
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

    def add(self, record: Base):
        self.session.add(record)
        self.session.commit()

    def find_all_plant_types(self, limit: int) -> List[PlantType]:
        query = select(PlantType).limit(limit)
        result = self.session.scalars(query)
        return result

    def find_plant_type_by_botanical_name(
            self, botanical_name_given: str) -> PlantType:
        query = select(PlantType).where(
            PlantType.botanical_name == botanical_name_given)
        result = self.session.scalars(query).one()
        return result
