from pydantic import BaseModel, ConfigDict, Field
from typing import List
from datetime import datetime


class LogPhotoCreateSchema(BaseModel):
    photo_link: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "photo_link": "https://pbs.twimg.com/media/EiSK6SgXsAAIQDC?format=jpg&name=small",
            }
        }


class LogPhotoSchema(LogPhotoCreateSchema):
    id: int = Field(...)
    log_id: int = Field(...)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "photo_link": "https://pbs.twimg.com/media/EiSK6SgXsAAIQDC?format=jpg&name=small",
                "id": 1
            }
        }


class LogCreateSchema(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    photos: List[LogPhotoCreateSchema] = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Mi buena petuña",
                "content": "Mi buena petuña es hermosa. Crece, crece y crece, y en verano me da mandarinas.",
                "photos":
                [
                    {
                        "photo_link": "https://pbs.twimg.com/media/EiSK6SgXsAAIQDC?format=jpg&name=small",
                    },
                    {
                        "photo_link": "https://pbs.twimg.com/media/EiSK6SgXsAAIQDC?format=jpg&name=small",
                    },
                ]
            }
        }


class LogSchema(LogCreateSchema):
    id: int = Field(...)
    created_at: datetime
    updated_at: datetime
    photos: List[LogPhotoSchema] = Field(...)

    class Config:
        from_attributes = True
