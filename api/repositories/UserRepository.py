from datetime import datetime
from uuid import UUID

from sqlalchemy import select

from config.db import AsyncSession
from config.security import get_password_hash
from models.DTOs import UserRequest
from models.entities import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: UserRequest):
        user = User(
            username=data.username,
            password=get_password_hash(data.password),
            name=data.name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            role=data.role,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def read(self):
        users = await self.db.execute(select(User))
        return users.scalars().all()

    async def read_by(self, id: UUID):
        user = await self.db.execute(select(User).where(User.id == id))
        return user.scalar()

    async def update(self, id: UUID, data: UserRequest):
        user = await self.read_by(id)
        if not user:
            return 404
        exists = await self.check_if_exists(data.username, data.email)
        if exists and exists.id != id:
            return 400
        user.username = data.username
        user.password = get_password_hash(data.password)
        user.name = data.name
        user.last_name = data.last_name
        user.email = data.email
        user.phone = data.phone
        user.role = data.role
        user.updated_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, id: UUID):
        user = await self.read_by(id)
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True

    async def check_if_exists(self, username: str = '', email: str = ''):
        user = await self.db.execute(
            select(User).where(
                (User.username == username) | (User.email == email)
            )
        )
        return user.scalar()
