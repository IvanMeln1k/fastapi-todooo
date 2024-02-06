from src.service.users import UsersService
from src.repository.users import UsersRepository
from src.repository.sessions import SessionsRepository


def get_users_service()->UsersService:
    return UsersService(UsersRepository(), SessionsRepository())