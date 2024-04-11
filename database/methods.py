from sqlalchemy import select

from database import async_session
from database.models import Games


async def get_games_data(duration: str = "", location: str = "", theme: str = ""):
    async with async_session() as session:
        print(", ".join([str(i) for i in [duration, location, theme]]))
        query = select(Games)
        if duration:
            query = query.where(Games.duration == duration)
        if location:
            query = query.where(Games.location == location)
        if theme:
            query = query.where(Games.theme == theme)
        return (await session.execute(query)).scalars().fetchall()
