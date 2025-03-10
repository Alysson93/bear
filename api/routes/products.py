from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from config.security import get_current_user
from models.DTOs import ProductRequest, ProductResponse
from models.entities import Product, User
from repositories import ProductRepository, get_product_repository

t_repository = Annotated[ProductRepository, Depends(get_product_repository)]
t_current_user = Annotated[User, Depends(get_current_user)]


router = APIRouter(prefix='/products', tags=['products'])


@router.get('/', response_model=list[ProductResponse])
async def read_products(repo: t_repository):
    products = await repo.read()
    return products


@router.get('/{id:uuid}', response_model=ProductResponse)
async def read_product_by_id(repo: t_repository, id: UUID):
    product = await repo.read_by(id)
    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found.'
        )
    return product


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=ProductResponse
)
async def create_product(
    repo: t_repository, current_user: t_current_user, data: ProductRequest
):
    product = await repo.create(data, current_user.id)
    return product


@router.put('/{id:uuid}', response_model=ProductResponse)
async def update_product(
    repo: t_repository,
    current_user: t_current_user,
    id: UUID,
    data: ProductRequest,
):
    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions.'
        )
    Product = await repo.update(id, data)
    if Product == 400:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Product already exists.',
        )
    elif Product == 404:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found.'
        )
    return Product


@router.delete('/{id:uuid}', status_code=HTTPStatus.NO_CONTENT)
async def delete_product(
    repo: t_repository, current_user: t_current_user, id: UUID
):
    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions.'
        )
    status = await repo.delete(id)
    if not status:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found.'
        )
