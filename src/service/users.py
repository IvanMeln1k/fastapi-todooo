from src.repository.users import UsersRepository
from src.hasher import hasher
from src.schemas.users import UserCreateSchema
from src.mail import send_email_confirmation
from src.tokens import (create_email_confirmation_token, create_user_id_token,
                        get_email_from_confirmation_token)

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
# from src.exceptions.exceptions import EmailAlreadyInUse


class EmailIsAlreadyInUse(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Email is already in use")


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")


class ServerError(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="Server error")


class UsersService:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo: UsersRepository = users_repo


    async def verify_email_user(self, session: AsyncSession, token: str):
        id = get_email_from_confirmation_token(token)

        user_by_id = await self.users_repo.get_one(session, id=id)

        if user_by_id is None:
            raise ServerError
        if user_by_id.is_email_verified:
            raise ServerError

        await self.users_repo.update_one(session, user_by_id.id, {
            "is_email_verified": True
        })

        await session.commit()


    async def get_user(self, session: AsyncSession, **filters):
        user = await self.users_repo.get_one(session, **filters)

        if user is None:
            raise ServerError

        return user

    async def create_user(self, session: AsyncSession, user: UserCreateSchema) -> int:
        user_by_email = await self.users_repo.get_one(session, email=user.email)

        if not user_by_email is None:
            if user_by_email.is_email_verified:
                raise EmailIsAlreadyInUse
            else:
                await self.users_repo.hard_delete_one(session, id=user_by_email.id)

        id = await self.users_repo.add_one(session, {
            "email": user.email,
            "name": user.name,
            "hash_password": hasher.hash_str(user.password)
        })

        await session.commit()

        token_confirmation_email = create_email_confirmation_token(id=id)
        send_email_confirmation(recipient_email=user.email,
                                recipient_name=user.email,
                                link_token=f"http://127.0.0.1:8000/auth/verify?token={token_confirmation_email}")

        return create_user_id_token(id)


    async def delete_user(self, session: AsyncSession, id: int):
        user_by_id = await self.users_repo.get_one(session, id=id)

        if user_by_id is None:
            raise UserNotFound

        user = await self.users_repo.delete_one(session, id)

        await session.commit()

        return user


    async def update_user(self, session: AsyncSession, id: int, data: dict):
        user_by_id = await self.users_repo.get_one(session, id=id)

        if user_by_id is None:
            raise UserNotFound

        user = await self.users_repo.update_one(session, id, data)

        await session.commit()

        return user