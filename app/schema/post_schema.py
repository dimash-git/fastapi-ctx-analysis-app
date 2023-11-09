from pydantic import BaseModel, Field


class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(default=None)
    content: str = Field(default=None)

    class Config:
        json_schema_extra = {
            "post_demo": {
                "title": "Some title",
                "content": "Some content about animals and nature"
            }
        }
