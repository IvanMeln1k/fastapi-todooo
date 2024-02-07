from fastapi import APIRouter, Depends, Body
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from src.tokens import get_user_id_from_token
from src.routers.dependencies import get_categories_service
from src.service.categories import CategoriesService
from src.schemas.categories import (CategoryCreateSchema, CategoryReturnSchema,
                                    CategoryUpdateSchema, CategorySchema)
from src.database import get_async_session


categories_router = APIRouter(prefix="/categories")


class CreateCategoryResponseModel(BaseModel):
    category: CategoryReturnSchema


@categories_router.post("/")
async def create_category(data: CategoryCreateSchema = Body(),
                          user_id: int = Depends(get_user_id_from_token),
                          categories_service: CategoriesService = Depends(get_categories_service),
                          session: AsyncSession = Depends(get_async_session)):
    category_id = await categories_service.add_category(session=session, user_id=user_id, data=data)
    return CategoryReturnSchema.model_validate({
        "id": category_id, **data.model_dump()}, from_attributes=True)


class GetCategoriesResponseModel(BaseModel):
    categories: list[CategoryReturnSchema]


@categories_router.get("/")
async def get_categories(title: str | None = None,
                         description: str | None = None,
                         user_id: int = Depends(get_user_id_from_token),
                         categories_service: CategoriesService = Depends(get_categories_service),
                         session: AsyncSession = Depends(get_async_session)):
    filters = dict()
    if not title is None: filters["title"] = title
    if not description is None: filters["description"] = description
    categories = await categories_service.get_all_category(session=session,
                                                           user_id=user_id,
                                                           **filters)
    categories = [CategoryReturnSchema.model_validate(item, from_attributes=True) for item in categories]
    return GetCategoriesResponseModel(
        categories=categories
    )


class GetCategoryResponseModel(BaseModel):
    category: CategoryReturnSchema


@categories_router.get("/{id}")
async def get_category(id: int,
                       user_id: int = Depends(get_user_id_from_token),
                       categories_service: CategoriesService = Depends(get_categories_service),
                       session: AsyncSession = Depends(get_async_session)):
    category = await categories_service.get_one_category(session, user_id, id)
    return GetCategoryResponseModel(
        category=CategoryReturnSchema.model_validate(category, from_attributes=True))


class UpdateCategoryResponseModel(BaseModel):
    category: CategoryReturnSchema


@categories_router.put("/{id}")
async def update_category(id: int,
                          data: CategoryUpdateSchema = Body(),
                          user_id: int = Depends(get_user_id_from_token),
                          categories_service: CategoriesService = Depends(get_categories_service),
                          session: AsyncSession = Depends(get_async_session)):
    category = await categories_service.update_category(session, user_id, data.model_dump(), id=id)
    return UpdateCategoryResponseModel(
        category=CategoryReturnSchema.model_validate(category, from_attributes=True)
    )


class DeleteCategoryResponseModel(BaseModel):
    category: CategoryReturnSchema


@categories_router.delete("/{id}")
async def delete_category(id: int,
                          user_id: int = Depends(get_user_id_from_token),
                          categories_service: CategoriesService = Depends(get_categories_service),
                          session: AsyncSession = Depends(get_async_session)):
    category = await categories_service.delete_category(session, user_id, id)
    return DeleteCategoryResponseModel(
        category=CategoryReturnSchema.model_validate(category, from_attributes=True)
    )



