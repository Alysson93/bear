from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from config.security import get_current_user
from models.DTOs import ProductRequest, ProductResponse
from models.entities import User
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
    product = await repo.update(id, data, current_user.id)
    if product == 404:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found.'
        )
    if product == 403:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions.'
        )
    return product


@router.delete('/{id:uuid}', status_code=HTTPStatus.NO_CONTENT)
async def delete_product(
    repo: t_repository, current_user: t_current_user, id: UUID
):
    status = await repo.delete(id, current_user.id)
    if status == 404:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found.'
        )
    if status == 403:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions.'
        )
