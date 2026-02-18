from typing import Optional, List
from pydantic import BaseModel, EmailStr, Json
from datetime import datetime, date
from enum import Enum

class Prescription(BaseModel):
    medicine: str 
    dosage: str 
    frequency: str 
    duration_days: int

class MedicalRecordsSchema(BaseModel):
    id: Optional[int] = None 
    appointment_id: int 
    vet_id: int 
    diagnosis: str 
    treatment: str
    prescriptions: Optional[List[Prescription]] 
    follow_up_date: Optional[date] = None