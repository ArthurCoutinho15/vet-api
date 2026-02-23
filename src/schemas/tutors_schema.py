from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

from src.schemas.animals_schema import AnimalOut
class TutorsSchema(BaseModel):
    id: Optional[int] = None
    name: str 
    cpf: str 
    email: EmailStr
    phone: str
    address: str
    created_at: datetime = datetime.now()
    
    class Config:
        orm_mode = True

class TutorUpdateSchema(BaseModel):
    name: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    
    class Config:
        orm_mode = True

class TutorWithAnimals(BaseModel):
    id: int
    name: str
    cpf: str
    email: str
    phone: str
    address: str

    animals: List[AnimalOut] = []

    class Config:
        orm_mode = True