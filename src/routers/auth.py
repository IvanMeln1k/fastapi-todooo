from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from email_validate import validate

from src.schemas.users import UserCreateSchema, UserAuthSchema, UserReturnSchema
from src.routers.dependencies import get_users_service
from src.service.users import UsersService
from src.database import get_async_session
from src.hasher import hasher
from src.tokens import create_user_id_token


auth_router = APIRouter(prefix="/auth")


class SignUpResponseSchema(BaseModel):
    token: str


class InvalidEmail(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid email")


@auth_router.post("/sign-up", status_code=201)
async def sign_up(user: UserCreateSchema,
                  user_service: UsersService = Depends(get_users_service),
                  session: AsyncSession = Depends(get_async_session))->SignUpResponseSchema:
    if not validate(user.email):
        raise InvalidEmail
    token = await user_service.create_user(session, user)
    return SignUpResponseSchema(token=token)


class VerifyResponseSchema(BaseModel):
    verified: bool


@auth_router.get("/verify")
async def verify(token: str,
                 user_service: UsersService = Depends(get_users_service),
                 session: AsyncSession = Depends(get_async_session))->VerifyResponseSchema:
    await user_service.verify_email_user(session, token)
    return VerifyResponseSchema(verified=True)


class SignInResponseSchema(BaseModel):
    user: UserReturnSchema
    access_token: str
    
    
class InvalidEmailOrPassword(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Incorrect email or password")


@auth_router.post("/sign-in")
async def sign_in(user: UserAuthSchema,
                  user_service: UsersService = Depends(get_users_service),
                  session: AsyncSession = Depends(get_async_session))->SignInResponseSchema:
    user_from_db = await user_service.get_user(session, email=user.email)
    if hasher.check_str(user_from_db.hash_password, user.password):
        return SignInResponseSchema(
            user=UserReturnSchema.model_validate(user_from_db, from_attributes=True),
            access_token=create_user_id_token(user_from_db.id)
        )
    else:
        raise InvalidEmailOrPassword