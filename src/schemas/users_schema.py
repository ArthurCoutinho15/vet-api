from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    vet = "vet"
    receptionist = "receptionist"
    

class UsersBaseSchema(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    role: RoleEnum 
    is_active: bool = True
    created_at: datetime = datetime.now()
    
    class Config:
        orm_mode = True
        
class UserCreateSchema(UsersBaseSchema):
    hashed_password: str
