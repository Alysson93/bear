from fastapi import Depends

from config.db import AsyncSession, get_db

from .UserRepository import UserRepository


def get_user_repository(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)
