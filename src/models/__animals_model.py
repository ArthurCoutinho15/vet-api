from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.core.configs import settings


class AnimalModel(settings.DBBaseModel):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    name = Column(String(100), nullable=False)
    species = Column(String(100), nullable=False)
    breed = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=False)
    weight_kg = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    tutor_id = Column(Integer, ForeignKey("tutors.id"), nullable=False)

    tutor = relationship("TutorModel", back_populates="animals")
    appointments = relationship("AppointmentsModel", back_populates="animal")
