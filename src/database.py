from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String

from typing import Annotated

from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


async_engine = create_async_engine(DB_URL)
async_sessionfactory = async_sessionmaker(async_engine)


async def get_async_session():
    async with async_sessionfactory() as session:
        yield session


str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }


    repr_cols_num = 3
    repr_cols = ()

    def __repr__(self):
        cols = []
        for index, col in enumerate(self.__table__.columns.keys()):
            if index < self.repr_cols_num or col in self.repr_cols:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<ROW>{self.__class__.__name__} {', '.join(cols)}</ROW>"