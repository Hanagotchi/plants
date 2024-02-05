from pydantic import BaseModel, Field
from typing import List, Optional


class LogPhotoSchema(BaseModel):
    id: Optional[int] = Field(None)
    photo_link: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "photo_link": "https://pbs.twimg.com/media/EiSK6SgXsAAIQDC?format=jpg&name=small",
                "id": 1
            }
        }


class LogSchema(BaseModel):
    id: Optional[int] = Field(None)
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
                    },
                    {
                        "photo_link": "https://pbs.twimg.com/media/EiSK6SgXsAAIQDC?format=jpg&name=small",
                    },
                ]
            }
        }

