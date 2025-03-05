from typing import Annotated

from fastapi import APIRouter, Depends

from models.DTOs import UserResponse
from models.entities import User
from repositories import UserRepository, get_user_repository

t_repository = Annotated[UserRepository, Depends(get_user_repository)]

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/', response_model=list[UserResponse])
async def read_users(repo: t_repository):
    users = await repo.read()
    return users
