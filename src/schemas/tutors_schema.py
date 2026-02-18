from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

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