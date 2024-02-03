from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from src.tokens import get_user_id_from_token
from src.database import get_async_session
from src.routers.dependencies import get_users_service
from src.service.users import UsersService
from src.schemas.users import UserReturnSchema, UserUpdateSchema

users_router = APIRouter(prefix="/users")


class GetUserResponseSchema(BaseModel):
    user: UserReturnSchema


@users_router.get("/")
async def get_user(id: int = Depends(get_user_id_from_token),
             session: AsyncSession = Depends(get_async_session),
             user_service: UsersService = Depends(get_users_service))->GetUserResponseSchema:
    user = await user_service.get_user(session, id=id)
    return GetUserResponseSchema(
        user=UserReturnSchema.model_validate(user, from_attributes=True)
    )


class UpdateUserResponseSchema(BaseModel):
    user: UserReturnSchema


@users_router.put("/")
async def update_user(id: int = Depends(get_user_id_from_token),
                      user: UserUpdateSchema = Body(),
                      session: AsyncSession = Depends(get_async_session),
                      user_service: UsersService = Depends(get_users_service))->UpdateUserResponseSchema:
    new_user = await user_service.update_user(session, id, user.model_dump())
    return UpdateUserResponseSchema(
        user=UserReturnSchema.model_validate(new_user, from_attributes=True)
    )


