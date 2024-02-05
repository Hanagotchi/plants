from pydantic import BaseModel, Field
from typing import List


class LogPhotoSchema(BaseModel):
    __tablename__ = "logs_photos"
    __table_args__ = {'schema': 'dev'}

    photo_link: str = Field(...)
    log_id: int = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "photo_link": "https://pbs.twimg.com/media/EiSK6SgXsAAIQDC?format=jpg&name=small",
                "log_id": 1
            }
        }


class LogSchema(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    photos: List[LogPhotoSchema] = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Mi buena petuña",
                "content": "Mi buena petuña es hermosa. Crece, crece y crece, y en verano me da mandarinas.",
                "photos":
                [
                    {
                        "photo_link": "https://pbs.twimg.com/media/EiSK6SgXsAAIQDC?format=jpg&name=small",
                        "log_id": 1
                    },
                    {
                        "photo_link": "https://pbs.twimg.com/media/EiSK6SgXsAAIQDC?format=jpg&name=small",
                        "log_id": 1
                    },
                ]
            }
        }

