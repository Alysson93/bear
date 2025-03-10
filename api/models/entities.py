from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'
    id: Mapped[UUID] = mapped_column(
        Uuid, init=False, primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(init=False, back_populates='products')
    created_at: Mapped[datetime] = mapped_column(
        DateTime, init=False, default=datetime.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, init=False, default=datetime.now()
    )


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(
        Uuid, init=False, primary_key=True, default=uuid4
    )
    username: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    products: Mapped[list['Product']] = relationship(
        init=False, back_populates='user', cascade='all, delete-orphan'
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, init=False, default=datetime.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, init=False, default=datetime.now()
    )
