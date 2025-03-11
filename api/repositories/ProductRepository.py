from datetime import datetime
from uuid import UUID

from sqlalchemy import select

from config.db import AsyncSession
from models.DTOs import ProductRequest
from models.entities import Product


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: ProductRequest, user_id: UUID):
        product = Product(
            name=data.name, description=data.description, user_id=user_id
        )
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def read(self):
        products = await self.db.execute(select(Product))
        return products.scalars().all()

    async def read_by(self, id: UUID):
        product = await self.db.execute(
            select(Product).where(Product.id == id)
        )
        return product.scalar()

    async def update(self, id: UUID, data: ProductRequest, user_id: UUID):
        product = await self.read_by(id)
        if not product:
            return 404
        if product.user_id != user_id:
            return 403
        product.name = data.name
        product.description = data.description
        product.updated_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete(self, id: UUID, user_id: UUID):
        product = await self.read_by(id)
        if not product:
            return 404
        if product.user_id != user_id:
            return 403
        await self.db.delete(product)
        await self.db.commit()
        return True
