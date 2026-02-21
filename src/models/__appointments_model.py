from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    Enum,
    Text,
)
from sqlalchemy.orm import relationship

from enum import Enum as BaseEnum

from src.core.configs import settings


class AppointmentStatusEnum(str, BaseEnum):
    scheduled = "scheduled"
    in_progress = "in progress"
    completed = "completed"
    cancelled = "cancelled"


class AppointmentsModel(settings.DBBaseModel):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vet_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    animal_id = Column(Integer, ForeignKey("animals.id"), nullable=False)
    scheduled_at = Column(DateTime, nullable=False, default=datetime.now)
    reason = Column(String(300), nullable=False)
    status = Column(Enum(AppointmentStatusEnum), default="scheduled", nullable=False)
    notes = Column(Text, nullable=True)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now)

    animal = relationship("AnimalModel", back_populates="appointments")

    vet = relationship(
        "UserModel", foreign_keys=[vet_id], back_populates="appointments"
    )

    creator = relationship(
        "UserModel", foreign_keys=[created_by], back_populates="created_appointments"
    )

    medical_record = relationship(
        "MedicalRecordsModel", 
        back_populates="appointment", 
        uselist=False # 1:1
    )
