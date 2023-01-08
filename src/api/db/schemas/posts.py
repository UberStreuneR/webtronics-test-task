from pydantic import BaseModel
from typing import Optional


class PostAdd(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class Post(PostAdd):
    post_id: int
    author_id: int

    class Config:
        orm_mode = True


class PostUpdate(BaseModel):
    title: Optional[str]
    body: Optional[str]
