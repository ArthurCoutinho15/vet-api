from typing import List

from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, status, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.appointments_schema import AppointmentSchema, AppointmentCreateSchema, AppointmentUpdatechema
from src.models.__appointments_model import AppointmentsModel

from sqlalchemy.future import select


class AppointmentsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    def __validate_role(self, current_user) -> bool:
        if current_user.role not in ["admin", "receptionist"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to create Appointments"
            )
    
    def __validate_time(self, schema: AppointmentCreateSchema):
        if schema.scheduled_at < datetime.now(timezone.utc) + timedelta(minutes=30):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointments must be scheduled at least 30 minutes in advance"

            )

            
    async def __validate_conflict(self, vet_id, schedule_time):
        end_time = schedule_time + timedelta(minutes=30)
        
        query = select(AppointmentsModel).where(
            AppointmentsModel.vet_id == vet_id,
            AppointmentsModel.scheduled_at < end_time,
            AppointmentsModel.scheduled_at > schedule_time - timedelta(minutes=30),
        )
        
        result = await self.db.execute(query)
        conflict = result.scalars().first()
        
        if conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Vet already has an appointment at this time"
            )
    
    
    async def create_appointment(self, schema: AppointmentCreateSchema, current_user) -> AppointmentsModel:
        self.__validate_role(current_user)
        self.__validate_time(schema)
        await self.__validate_conflict(vet_id=schema.vet_id, schedule_time=schema.scheduled_at)
        
        appointment: AppointmentsModel = AppointmentsModel(**schema.dict())
        
        self.db.add(appointment)
        await self.db.commit()
        await self.db.refresh(appointment)
        
        return appointment
    
    async def get_appointments(self) -> List[AppointmentSchema]:
        async with self.db as session:
            query = select(AppointmentsModel)
            result = await session.execute(query)
            
            appointments = result.scalars().unique().all()
            
            return appointments
        
    async def get_appointment(self, appointment_id: int) -> AppointmentSchema:
        async with self.db as session:
            query = select(AppointmentsModel).where(AppointmentsModel.id == appointment_id)
            result = await session.execute(query)
            
            appointment = result.scalars().unique().one_or_none()
            
            return appointment
        
    async def put_appointment(self, appointment_id: int, schema: AppointmentUpdatechema) -> AppointmentSchema:
        async with self.db as session:
            query = select(AppointmentsModel).filter(AppointmentsModel.id == appointment_id)
            result = await session.execute(query)
            appointment_up = result.scalars().unique().one_or_none()

            if not appointment_up:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found."
                )

            if schema.animal_id:
                appointment_up.animal_id = schema.animal_id
            if schema.vet_id:
                appointment_up.vet_id = schema.vet_id
            if schema.reason:
                appointment_up.reason = schema.reason
            if schema.notes:
                appointment_up.notes = schema.notes
            if schema.created_by:
                appointment_up.created_by = schema.created_by

            await session.commit()

            return appointment_up
        
    async def delete_appointment(self, appointment_id: int):
        async with self.db as session:
            query = select(AppointmentsModel).filter(AppointmentsModel.id == appointment_id)
            result = await session.execute(query)

            appointment_del = result.scalars().unique().one_or_none()

            if not appointment_del:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found."
                )

            await session.delete(appointment_del)
            await session.commit()

            return Response(
                content="Appointment Deleted Successfully",
                status_code=status.HTTP_204_NO_CONTENT,
            )