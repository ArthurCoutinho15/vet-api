from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime
from enum import Enum as BaseEnum

from src.core.configs import settings


class UserRoleEnum(str, BaseEnum):
    admin = "admin"
    vet = "vet"
    receptionist = "receptionist"


class UserModel(settings.DBBaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    password = Column(String(256), nullable=False)
    role = Column(Enum(UserRoleEnum), nullable=False)
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime, default=datetime.now)

    appointments = relationship(
        "AppointmentsModel",
        back_populates="vet",
        foreign_keys="AppointmentsModel.vet_id"
    )
    created_appointments = relationship(
        "AppointmentsModel",
        back_populates="creator",
        foreign_keys="AppointmentsModel.created_by",
    )
    medical_records = relationship("MedicalRecordsModel")
