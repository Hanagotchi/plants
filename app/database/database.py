from sqlalchemy import create_engine, select, delete, engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from os import environ

from app.database.models.example import Example
from app.database.models.Log import Log
from app.database.models.base import Base
from typing import List
from datetime import date

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

    def find_by_id(self, id_received: str) -> Example:
        query = select(Example).where(Example.id == id_received)
        result = self.session.scalars(query).one()
        return result

    def find_all(self, limit: int) -> List[Example]:
        query = select(Example).limit(limit)
        result = self.session.scalars(query)
        return result

    def find_logs_between(self,
                          plant_id: int,
                          cleft: date,
                          cright: date) -> List[Log]:
        # where(Log.plant_id == plant_id).\
        query = select(Log).\
                where(Log.created_at.between(cleft, cright)).\
                order_by(Log.created_at.asc())
        result = self.session.scalars(query)
        return result
