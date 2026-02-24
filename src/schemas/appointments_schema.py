from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from enum import Enum

from src.schemas.medical_records_schema import MedicalRecordHistorySchema

class AppointmentStatusEnum(str, Enum):
    scheduled = "scheduled"
    in_progress = "in progress"
    completed = "completed"
    cancelled = "cancelled"

class AppointmentSchema(BaseModel):
    id: Optional[int] = None
    animal_id: int
    vet_id: int 
    scheduled_at: datetime = datetime.now()
    reason: str 
    status: AppointmentStatusEnum = "scheduled"
    notes: str 
    created_by: int 
    created_at: datetime = datetime.now()
    
    class Config:
        orm_mode = True

class AppointmentCreateSchema(BaseModel):
    animal_id: int
    vet_id: int 
    reason: str 
    notes: str 
    created_by: int 
    
    class Config:
        orm_mode = True
        
class AppointmentHistorySchema(BaseModel):
    id: int
    scheduled_at: datetime
    status: str
    reason: str | None = None
    notes: str | None = None
    medical_record: MedicalRecordHistorySchema | None = None

    class Config:
        from_attributes = True