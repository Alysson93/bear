from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class UserRequest(BaseModel):
    username: str
    password: str
    name: str
    last_name: str
    email: EmailStr
    phone: str
    role: str


class UserResponse(BaseModel):
    id: UUID
    username: str
    name: str
    last_name: str
    email: EmailStr
    phone: str
    role: str
    created_at: datetime
    updated_at: datetime
