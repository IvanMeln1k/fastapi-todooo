from src.service.users import UsersService
from src.repository.users import UsersRepository
from src.repository.sessions import SessionsRepository
from src.repository.categories import CategoriesRepository
from src.service.categories import CategoriesService


def get_users_service() -> UsersService:
    return UsersService(UsersRepository(), SessionsRepository())


def get_categories_service() -> CategoriesService:
    return CategoriesService(CategoriesRepository(), UsersRepository())

