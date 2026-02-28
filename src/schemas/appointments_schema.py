from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime, date, timezone
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
    status: AppointmentStatusEnum = AppointmentStatusEnum.scheduled
    notes: str
    created_by: int
    created_at: datetime = datetime.now()

    class Config:
        orm_mode = True


class AppointmentCreateSchema(BaseModel):
    animal_id: int
    vet_id: int
    scheduled_at: datetime
    reason: str
    notes: str
    created_by: int

    class Config:
        orm_mode = True


class AppointmentUpdatechema(BaseModel):
    animal_id: Optional[int] = None
    vet_id: Optional[int] = None
    scheduled_at: Optional[datetime] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
    created_by: Optional[int] = None

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

class AppointmentPatchStatusSchema(BaseModel):
    status: AppointmentStatusEnum