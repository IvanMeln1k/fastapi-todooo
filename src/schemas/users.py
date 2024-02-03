from pydantic import BaseModel
import datetime


class UserSchema(BaseModel):
    id: int
    email: str
    name: str
    is_email_verified: bool
    created_at: datetime.datetime
    hash_password: str


class UserCreateSchema(BaseModel):
    email: str
    name: str
    password: str


class UserAuthSchema(BaseModel):
    email: str
    password: str


class UserReturnSchema(BaseModel):
    id: int
    email: str
    name: str
    is_email_verified: bool
    created_at: datetime.datetime


class UserUpdateSchema(BaseModel):
    name: str