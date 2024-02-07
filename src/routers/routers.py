from src.routers.auth import auth_router
from src.routers.users import users_router
from src.routers.categories import categories_router


all_routers = [auth_router, users_router, categories_router]

