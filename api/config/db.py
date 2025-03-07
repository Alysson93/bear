from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL, echo=True)

session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    global session
    async with session() as s:
        yield s
