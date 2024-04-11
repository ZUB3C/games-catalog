import asyncio

from sqlalchemy import Column, Integer, String, delete
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from config import DATABASE_NAME
from database.data import GAMES_DATA, GameData
from misc import PathControl


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Games(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=False, nullable=False)
    condition = Column(String, unique=False, nullable=False)

    duration = Column(String, unique=False, nullable=False)
    location = Column(String, unique=False, nullable=False)
    theme = Column(String, unique=False, nullable=False)


async def add_data(data: list[GameData]) -> None:
    data = [
        Games(
            title=i.title,
            condition=i.condition,
            duration=str(i.duration),
            location=str(i.location),
            theme=str(i.theme),
        )
        for i in data
    ]
    async with async_session() as session, session.begin():
        await session.execute(delete(Games))
        session.add_all(data)


async def register_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await add_data(GAMES_DATA)


engine: AsyncEngine = create_async_engine(
    url=f'sqlite+aiosqlite:///{PathControl.get(f"database/{DATABASE_NAME}")}'
)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

if __name__ == "__main__":
    asyncio.run(register_models())
