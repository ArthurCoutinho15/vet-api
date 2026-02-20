from typing import List, Optional, Any

from fastapi import APIRouter, status, HTTPException, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.models.__appointments_model import AppointmentsModel

from src.schemas.appointments_schema import AppointmentSchema, AppointmentCreateSchema

from src.core.deps import get_session

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AppointmentCreateSchema)
async def post_appointment(appointment: AppointmentCreateSchema, db: AsyncSession = Depends(get_session)):
    new_appointment: AppointmentsModel = AppointmentsModel(
        animal_id = appointment.animal_id,
        vet_id = appointment.vet_id,
        reason = appointment.reason,
        notes = appointment.notes,
        created_by = appointment.created_by
    ) 
    
    db.add(new_appointment)
    await db.commit()
    
    return new_appointment

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[AppointmentSchema])
async def get_appointments(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AppointmentsModel)
        results = await session.execute(query)
        
        appointments: List[AppointmentsModel] = results.scalars().unique().all()
        
        return appointments
    
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=AppointmentSchema)
async def get_appointment(appointment_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AppointmentsModel).filter(AppointmentsModel.id == appointment_id)
        results = await session.execute(query)
        
        appointment: AppointmentsModel = results.scalars().unique().one_or_none()
        
        return appointment
    
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=AppointmentSchema)
async def put_appointment(appointment_id: int, appointment: AppointmentCreateSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AppointmentsModel).filter(AppointmentsModel.id == appointment_id)
        result = await session.execute(query)
        
        appointment_up = result.scalars().unique().one_or_none()
        
        if not appointment_up:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found.")
        
        if appointment.animal_id:
            appointment_up.animal_id = appointment.animal_id
        if appointment.vet_id:
            appointment_up.vet_id = appointment.vet_id
        if appointment.reason:
            appointment_up.reason = appointment.reason
        if appointment.notes:
            appointment_up.notes = appointment.notes
        if appointment.created_by:
            appointment_up.created_by = appointment.created_by
        
        await session.commit()
        
        return appointment_up

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(appointment_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AppointmentsModel).filter(AppointmentsModel.id == appointment_id)
        result = await session.execute(query)
        
        appointment_del = result.scalars().unique().one_or_none()
        
        if not appointment_del:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found.")
        
        await session.delete(appointment_del)
        await session.commit()
        
        return Response(content="Appointment Deleted Successfully", status_code=status.HTTP_204_NO_CONTENT)


# TODO Criar rota para pegar agenda do veterinário por perído
#  Criar regras de negócio