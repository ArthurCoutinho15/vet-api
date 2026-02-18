from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime, date

from tutors_schema import TutorsSchema

class AnimalsSchema(BaseModel):
    id: Optional[int] = None 
    name: str 
    species: str
    breed: str
    birth_date: date
    weitgh_kg: float
    created_at: datetime = datetime.now()

    class Config:
        orm_mode = True    
        
class AnimalsSchemaTutors(AnimalsSchema):
    tutor_id: int 