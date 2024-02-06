import datetime

from src.repository.users import UsersRepository
from src.hasher import hasher
from src.schemas.users import UserCreateSchema, UserAuthSchema, UserReturnSchema
from src.mail import send_email_confirmation
from src.tokens import (create_email_confirmation_token, create_user_id_token,
                        get_id_from_email_confirmation_token, create_random_string)
from src.repository.sessions import SessionsRepository
from src.config import EXP_REFRESH
from src.hasher import hasher

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException


class EmailIsAlreadyInUse(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Email is already in use")


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")


class ServerError(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="Server error")


class InvalidEmailOrPassword(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Incorrect email or password")


class ExpiredSession(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Expired session")


class InvalidRefreshToken(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid refresh token")


class UsersService:
    def __init__(self, users_repo: UsersRepository, sessions_repo: SessionsRepository):
        self.users_repo: UsersRepository = users_repo
        self.sessions_repo: SessionsRepository = sessions_repo


    async def verify_email_user(self, session: AsyncSession, token: str):
        id = get_id_from_email_confirmation_token(token)

        user_by_id = await self.users_repo.get_one(session, id=id)

        if user_by_id is None:
            raise ServerError
        if user_by_id.is_email_verified:
            raise ServerError

        await self.users_repo.update_one(session, user_by_id.id, {
            "is_email_verified": True
        })

        await session.commit()


    async def get_user(self, session: AsyncSession, id: int):
        user = await self.users_repo.get_one(session, id=id)

        if user is None:
            raise ServerError

        return user

    async def auth_user(self, session: AsyncSession, user: UserAuthSchema):
        user_from_db = await self.users_repo.get_one(session, email=user.email)

        if user_from_db is None:
            raise ServerError

        refresh_token = create_random_string()
        await self.__check_sessions_count(session, user_from_db.id)
        await self.sessions_repo.add_one(session, {
            "token": refresh_token,
            "expires_in": datetime.datetime.utcnow() + EXP_REFRESH,
            "user_id": user_from_db.id
        })
        await session.commit()

        access_token = create_user_id_token(id=user_from_db.id)

        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

        if hasher.check_str(user_from_db.hash_password, user.password):
            return {
                "tokens": tokens,
                "user": UserReturnSchema.model_validate(user_from_db, from_attributes=True)
            }
        else:
            raise InvalidEmailOrPassword

    async def __check_sessions_count(self, session: AsyncSession, user_id: int):
        user_sessions = await self.sessions_repo.get_all(session, user_id=user_id)
        if len(user_sessions) >= 5:
            user_sessions.sort(key=lambda x:x.expires_in)
            await self.sessions_repo.delete(session, id=user_sessions[0].id)

    async def __check_sessions_expire(self, session: AsyncSession, token):
        user_session = await self.sessions_repo.get_one(session, token=token)
        if user_session is None:
            raise InvalidRefreshToken
        if user_session.expires_in <= datetime.datetime.utcnow():
            await self.sessions_repo.delete(session, id=user_session.id)
            await session.commit()
            raise ExpiredSession

    async def refresh_tokens(self, session: AsyncSession, refresh_token: str):
        await self.__check_sessions_expire(session, token=refresh_token)
        new_refresh_token = create_random_string()
        user_session = await self.sessions_repo.update(session, token=refresh_token, data={
            "token": new_refresh_token,
            "expires_in": datetime.datetime.utcnow() + EXP_REFRESH,
        })
        await session.commit()

        user_id = user_session.user_id
        new_access_token = create_user_id_token(id=user_id)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
        }

    async def create_user(self, session: AsyncSession, user: UserCreateSchema):
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

        refresh_token = create_random_string()

        await self.sessions_repo.add_one(session, {
            "token": refresh_token,
            "expires_in": datetime.datetime.utcnow() + EXP_REFRESH,
            "user_id": id
        })

        await session.commit()

        token_confirmation_email = create_email_confirmation_token(id=id)
        send_email_confirmation(recipient_email=user.email,
                                recipient_name=user.email,
                                link_token=f"http://127.0.0.1:8000/auth/verify?token={token_confirmation_email}")

        return {
            "access_token": create_user_id_token(id),
            "refresh_token": refresh_token
        }


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