from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime

from src.core.configs import settings


class TutorModel(settings.DBBaseModel):
    __tablename__ = "tutors"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False, index=True)
    email = Column(String(200), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(String(300), nullable=True)

    animals = relationship("AnimalModel", back_populates="tutor")
