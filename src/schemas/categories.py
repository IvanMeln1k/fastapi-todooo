from pydantic import BaseModel


class CategorySchema(BaseModel):
    id: int
    title: str
    description: str
    user_id: int


class CategoryCreate(BaseModel):
    title: str
    description: str


class CategoryReturn(BaseModel):
    id: int
    title: str
    description: str


