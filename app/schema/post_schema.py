from pydantic import BaseModel, Field
from datetime import datetime


class PostBase(BaseModel):
    title: str = Field(default=None)
    description: str = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Some title",
                "description": "Some description about animals and nature"
            }
        }


class Post(PostBase): # при изменении данных и при получении
    id: int = Field(default=None)
    date: datetime = Field(default_factory=datetime.now)
    user_id: int = Field(default=None)
