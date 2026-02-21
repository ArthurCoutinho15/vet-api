from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Json
from datetime import datetime, date
from enum import Enum

class Prescription(BaseModel):
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
    prescriptions: Optional[List[Prescription]]
    follow_up_date: Optional[date]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True