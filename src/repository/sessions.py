import datetime

from src.models.sessions import Sessions
from src.schemas.sessions import SessionSchema

from sqlalchemy import delete, update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession


def tuple_to_session(data: tuple) -> SessionSchema:
    return SessionSchema(
        id=data[0],
        token=data[1],
        expires_in=data[2],
        user_id=data[3]
    )


class SessionsRepository:
    model = Sessions

    async def get_all(self, session: AsyncSession, **filters) -> list[SessionSchema]:
        stmt = (
            select(self.model)
            .filter_by(**filters)
        )
        res = await session.execute(stmt)
        res = res.scalars().all()
        res = [SessionSchema.model_validate(item, from_attributes=True) for item in res]
        return res

    async def get_one(self, session: AsyncSession, **filters) -> SessionSchema | None:
        stmt = (
            select(self.model)
            .filter_by(**filters)
            .limit(1)
        )
        res = await session.execute(stmt)
        res = res.scalar_one_or_none()

        if res is None:
            return None

        res = SessionSchema.model_validate(res, from_attributes=True)
        return res

    async def delete(self, session: AsyncSession, **filters) -> bool:
        stmt = (
            delete(self.model)
            .filter_by(**filters)
        )
        await session.execute(stmt)
        return True

    async def update(self, session: AsyncSession, token: str, data: dict) -> SessionSchema | None:
        stmt = (
            update(self.model)
            .values(**data)
            .filter_by(token=token)
            .returning(self.model.id, self.model.token, self.model.expires_in, self.model.user_id)
        )
        res = await session.execute(stmt)
        res = res.one_or_none()
        if res is None:
            return None
        return tuple_to_session(res)

    async def add_one(self, session: AsyncSession, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await session.execute(stmt)
        id = res.scalar_one()
        return id