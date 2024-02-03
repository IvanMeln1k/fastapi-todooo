from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select

from src.models.users import Users

from src.schemas.users import UserSchema


def tuple_to_user(data: tuple):
    return UserSchema(
        id=data[0],
        email=data[1],
        name=data[2],
        is_email_verified=data[3],
        created_at=data[4],
        hash_password=data[5]
    )


class UsersRepository:
    model = Users

    async def get_one(self, session: AsyncSession, **filters) -> UserSchema | None:
        stmt = (
            select(self.model)
            .filter_by(**filters)
        )
        res = await session.execute(stmt)
        res = res.scalar_one_or_none()

        if res is None:
            return None

        if res.is_deleted:
            return None

        user = UserSchema.model_validate(res, from_attributes=True)
        return user

    async def add_one(self, session: AsyncSession, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await session.execute(stmt)
        id = res.scalar_one()
        # await session.commit()
        return id

    async def delete_one(self, session: AsyncSession, id: int) -> UserSchema:
        stmt = (
            update(self.model)
            .values(is_deleted=True)
            .filter_by(id=id)
            .returning(self.model.id, self.model.email, self.model.name,
                       self.model.is_email_verified, self.model.created_at, self.model.hash_password)
        )
        res = await session.execute(stmt)
        res = res.one()
        user = tuple_to_user(res)
        # await session.commit()
        return user

    async def update_one(self, session: AsyncSession, id: int, data: dict) -> UserSchema:
        stmt = (
            update(self.model)
            .values(**data)
            .filter_by(id=id)
            .returning(self.model.id, self.model.email, self.model.name,
                       self.model.is_email_verified, self.model.created_at, self.model.hash_password)
        )
        res = await session.execute(stmt)
        res = res.one()
        user = tuple_to_user(res)
        print(user)
        return user
