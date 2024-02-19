from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

link = "https://pbs.twimg.com/media/EiSK6SgXsAAIQDC?format=jpg&name=small"


class LogPhotoCreateSchema(BaseModel):
    photo_link: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "photo_link": link,
            }
        }


class LogPhotoSchema(LogPhotoCreateSchema):
    id: int = Field(...)
    log_id: int = Field(...)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "photo_link": link,
                "id": 1
            }
        }


class LogCreateSchema(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    photos: List[LogPhotoCreateSchema] = Field(...)
    plant_id: int = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Mi buena petuña",
                "content": ("Mi buena petuña es hermosa. "
                            "Crece, crece y crece, "
                            "y en verano me da mandarinas."),
                "plant_id": 1,
                "photos":
                [
                    {
                        "photo_link": link,
                    },
                    {
                        "photo_link": link,
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
        json_schema_extra = {
            "example": {
                "id": 102,
                "title": "Mi buena petuña",
                "content": ("Mi buena petuña es hermosa. "
                            "Crece, crece y crece, "
                            "y en verano me da mandarinas."),
                "plant_id": 1,
                "photos":
                [
                    {
                        "photo_link": link,
                    },
                    {
                        "photo_link": link,
                    },
                ]
            }
        }


class LogPartialUpdateSchema(BaseModel):
    title: Optional[str] = Field(None)
    content: Optional[str] = Field(None)
    plant_id: Optional[int] = Field(None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Mi buena petuña",
                "content": ("Mi buena petuña es hermosa. "
                            "Crece, crece y crece, "
                            "y en verano me da mandarinas."),
                "plant_id": 1
            }
        }