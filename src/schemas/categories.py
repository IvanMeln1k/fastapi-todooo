from pydantic import BaseModel


class CategorySchema(BaseModel):
    id: int
    title: str
    description: str
    user_id: int


class CategoryCreateSchema(BaseModel):
    title: str
    description: str


class CategoryReturnSchema(BaseModel):
    id: int
    title: str
    description: str


class CategoryUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None