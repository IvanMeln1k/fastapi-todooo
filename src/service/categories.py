from src.repository.categories import CategoriesRepository
from src.schemas.categories import CategoryCreateSchema
from src.repository.users import UsersRepository

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException


class NotFoundCategory(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Category not found")


class Forbidden(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Forbidden")


class RequestHasNotUpdateData(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Request has not update data")


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")


class CategoriesService:
    def __init__(self, categories_repo: CategoriesRepository, users_repo: UsersRepository):
        self.categories_repo = categories_repo
        self.users_repo = users_repo

    async def __check_user(self, session: AsyncSession, user_id):
        user = await self.users_repo.get_one(session, id=user_id)
        if user is None:
            raise UserNotFound

    async def add_category(self, session: AsyncSession, user_id: int, data: CategoryCreateSchema):
        await self.__check_user(session, user_id)
        category = await self.categories_repo.add_one(session, {
            **data.model_dump(),
            "user_id": user_id,
        })
        await session.commit()
        return category

    async def delete_category(self, session: AsyncSession, user_id: int, id: int):
        await self.__check_user(session, user_id)
        categories = await self.categories_repo.delete(session, user_id=user_id, id=id)
        if len(categories) == 0:
            raise NotFoundCategory
        category = categories[0]
        await session.commit()
        return category

    async def update_category(self, session: AsyncSession, user_id: int, data: dict, **filters):
        await self.__check_user(session, user_id)
        update_data = dict()
        for key, value in data.items():
            if not value is None:
                update_data[key] = value
        if update_data == {}:
            raise RequestHasNotUpdateData
        category = await self.categories_repo.update(session, update_data, user_id=user_id, **filters)
        if category is None:
            raise NotFoundCategory
        await session.commit()
        return category

    async def get_all_category(self, session: AsyncSession, user_id: int, **filters):
        await self.__check_user(session, user_id)
        categories = await self.categories_repo.get_all(session, user_id=user_id, **filters)
        return categories

    async def get_one_category(self, session: AsyncSession, user_id: int, id: int):
        await self.__check_user(session, user_id)
        category = await self.categories_repo.get_one(session=session, user_id=user_id, id=id)
        if category is None:
            raise NotFoundCategory
        return category



