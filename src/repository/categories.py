from sqlalchemy import update, delete, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.categories import Categories
from src.schemas.categories import CategorySchema


def tuple_to_category(data: tuple):
    return CategorySchema(
        id=data[0],
        title=data[1],
        description=data[2],
        user_id=data[3]
    )


class CategoriesRepository:
    model = Categories

    async def add_one(self, session: AsyncSession, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await session.execute(stmt)
        id = res.scalar_one()
        return id

    async def get_one(self, session: AsyncSession, **filters):
        stmt = select(self.model).filter_by(**filters).limit(1)
        res = await session.execute(stmt)
        res = res.scalar_one_or_none()
        if res is None:
            return None
        category = CategorySchema.model_validate(res, from_attributes=True)
        return category

    async def get_all(self, session: AsyncSession, **filters):
        stmt = select(self.model).filter_by(**filters)
        res = await session.execute(stmt)
        res = res.scalars().all()
        categories = [CategorySchema.model_validate(item, from_attributes=True) for item in res]
        return categories

    async def delete(self, session: AsyncSession, **filters):
        stmt = (
            delete(self.model)
            .filter_by(**filters)
            .returning(self.model.id, self.model.title, self.model.description, self.model.user_id)
        )
        res = await session.execute(stmt)
        res = res.all()
        categories = [tuple_to_category(item) for item in res]
        return categories





