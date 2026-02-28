from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Json
from datetime import datetime, date
from enum import Enum

class PrescriptionSchema(BaseModel):
    medicine: str 
    dosage: str 
    frequency: str 
    duration_days: int

class MedicalRecordSchema(BaseModel):
    id: Optional[int]
    appointment_id: int
    vet_id: int
    diagnosis: str
    treatment: str
    prescriptions: Optional[List[PrescriptionSchema]]
    follow_up_date: Optional[date]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class MedicalRecordCreateSchema(BaseModel):
    appointment_id: int
    vet_id: int
    diagnosis: str
    treatment: str
    prescriptions: Optional[List[PrescriptionSchema]]
    follow_up_date: Optional[date]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
        
class MedicalRecordUpdateSchema(BaseModel):
    appointment_id: Optional[int] = None
    vet_id: Optional[int] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    prescriptions: Optional[List[PrescriptionSchema]] = None
    follow_up_date: Optional[date] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        
class MedicalRecordHistorySchema(BaseModel):
    id: int
    diagnosis: str
    treatment: str | None = None
    prescriptions: list[PrescriptionSchema] = []
    follow_up_date: date | None = None
    created_at: datetime

    class Config:
        from_attributes = True