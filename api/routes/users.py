from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from models.DTOs import UserRequest, UserResponse
from repositories import UserRepository, get_user_repository

t_repository = Annotated[UserRepository, Depends(get_user_repository)]

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/', response_model=list[UserResponse])
async def read_users(repo: t_repository):
    users = await repo.read()
    return users


@router.get('/{id:uuid}', response_model=UserResponse)
async def read_user_by_id(repo: t_repository, id: UUID):
    user = await repo.read_by(id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )
    return user


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_user(repo: t_repository, data: UserRequest):
    user = await repo.check_if_exists(data.username, data.email)
    if user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='User already exists.'
        )
    user = await repo.create(data)
    return user


@router.put('/{id:uuid}')
async def update_user(repo: t_repository, id: UUID, data: UserRequest):
    user = await repo.update(id, data)
    if user == 400:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='User already exists.'
        )
    elif user == 404:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )
    return user


@router.delete('/{id:uuid}', status_code=HTTPStatus.NO_CONTENT)
async def delete_user(repo: t_repository, id: UUID):
    status = await repo.delete(id)
    if not status:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )
