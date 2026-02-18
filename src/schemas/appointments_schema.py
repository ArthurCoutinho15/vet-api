from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from enum import Enum

class AppointmentStatusEnum(str, Enum):
    scheduled = "scheduled"
    in_progress = "in progress"
    completed = "completed"
    cancelled = "cancelled"

class AppointmentSchema(BaseModel):
    id: Optional[int] = None
    animal_id: int
    vet_id: int 
    scheduled_at: datetime
    reason: str 
    status: AppointmentStatusEnum = "scheduled"
    notes: str 
    created_by: int 
    created_at: datetime = datetime.now()