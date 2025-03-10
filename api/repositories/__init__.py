from fastapi import Depends

from config.db import AsyncSession, get_db

from .ProductRepository import ProductRepository
from .UserRepository import UserRepository


def get_user_repository(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)


def get_product_repository(db: AsyncSession = Depends(get_db)):
    return ProductRepository(db)
