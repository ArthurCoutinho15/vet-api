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
    JSON
)
from sqlalchemy.orm import relationship

from datetime import datetime

from src.core.configs import settings

class MedicalRecordsModel(settings.DBBaseModel):
    __tablename__ = "medical_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    appointment_id = Column(Integer, ForeignKey("appointments.id", ondelete="CASCADE"), nullable=False)
    vet_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    diagnosis = Column(Text, nullable=False)
    treatment = Column(Text, nullable=False)
    prescriptions = Column(JSON, nullable=True)
    follow_up_date = Column(Date, nullable=True)
    created_at = Column(Date, default=datetime.now)
    updated_at = Column(Date, default=datetime.now)
    
    appointment = relationship("AppointmentsModel", back_populates="medical_record")
    vet = relationship("UserModel", lazy="selectin")
    