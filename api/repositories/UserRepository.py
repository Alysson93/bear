from sqlalchemy import select

from config.db import AsyncSession
from models.entities import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def read(self):
        users = await self.db.execute(select(User))
        return users.scalars().all()
