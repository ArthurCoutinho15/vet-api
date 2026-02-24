from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date
from src.schemas.appointments_schema import AppointmentHistorySchema


class AnimalsSchema(BaseModel):
    id: Optional[int] = None 
    name: str 
    species: str
    breed: str
    birth_date: date
    weight_kg: float
    created_at: Optional[datetime] = datetime.now()

    class Config:
        orm_mode = True    
        
class AnimalsSchemaTutors(AnimalsSchema):
    tutor_id: int 
    
    
class AnimalOut(BaseModel):
    id: int
    name: str
    species: str
    breed: str
    weight_kg: float

    class Config:
        orm_mode = True
        
class AnimalHistorySchema(BaseModel):
    id: int
    name: str
    species: str
    breed: str | None = None
    birth_date: date
    weight_kg: float | None = None

    appointments: list[AppointmentHistorySchema] = []

    class Config:
        from_attributes = True