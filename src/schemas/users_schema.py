from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    vet = "vet"
    receptionist = "receptionist"
    

class UsersBaseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool
    created_at: datetime = datetime.now()

    class Config:
        orm_mode = True
        
class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleEnum
