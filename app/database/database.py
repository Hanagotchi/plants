from sqlalchemy import create_engine, select, delete, engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from os import environ

from app.database.models.plants import Plants
from typing import List

load_dotenv()


class SQLAlchemyClient():
    db_url = engine.URL.create(
        "postgresql",
        database=environ["PLANTS_DB"],
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

    def clean_table(self, table: Plants): #Union[Example, ...]):
        query = delete(table)
        self.session.execute(query)
        self.session.commit()

    def add(self, record: Plants): #Union[Example, ...]):
        self.session.add(record)
        self.session.commit()

    def find_by_id(self, id_received: str) -> Plants:
        query = select(Plants).where(Plants.id == id_received)
        result = self.session.scalars(query).one()
        return result

    def find_all(self, limit: int) -> List[Plants]:
        query = select(Plants).limit(limit)
        result = self.session.scalars(query)
        return result
    
    def find_all_by_user(self, id_user: str, limit: int) -> List[Plants]:
        query = select(Plants).where(Plants.user_id == id_user).limit(limit)
        result = self.session.scalars(query)
        return result