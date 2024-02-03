from src.service.users import UsersService
from src.repository.users import UsersRepository


def get_users_service()->UsersService:
    return UsersService(UsersRepository())