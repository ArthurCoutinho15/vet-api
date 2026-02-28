from typing import List, Optional, Any

from datetime import datetime, timezone

from fastapi import APIRouter, status, HTTPException, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.schemas.appointments_schema import (
    AppointmentSchema,
    AppointmentCreateSchema,
    AppointmentUpdatechema,
    AppointmentPatchStatusSchema,
)

from src.services.appointments_service import AppointmentsService

from src.core.deps import get_session, get_current_user

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=AppointmentCreateSchema
)
async def post_appointment(
    appointment: AppointmentCreateSchema,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    appointment_service = AppointmentsService(db)
    new_appointment = await appointment_service.create_appointment(
        schema=appointment, current_user=user
    )

    return new_appointment


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[AppointmentSchema])
async def get_appointments(
    db: AsyncSession = Depends(get_session), user=Depends(get_current_user)
):
    appointment_service = AppointmentsService(db)

    appointments = await appointment_service.get_appointments()

    return appointments


@router.get(
    "/{appointment_id}",
    status_code=status.HTTP_200_OK,
    response_model=AppointmentSchema,
)
async def get_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    appointment_service = AppointmentsService(db)

    appointment = await appointment_service.get_appointment(appointment_id)

    return appointment


@router.put(
    "/{appointment_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=AppointmentSchema,
)
async def put_appointment(
    appointment_id: int,
    appointment: AppointmentUpdatechema,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    appointment_service = AppointmentsService(db)

    appointment = await appointment_service.put_appointment(
        appointment_id, schema=appointment
    )

    return appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    appointment_service = AppointmentsService(db)

    appointment = await appointment_service.delete_appointment(appointment_id)

    return appointment

@router.patch("/{appointment_id}", status_code=status.HTTP_202_ACCEPTED)
async def patch_appointment(
    appointment_id: int,
    appointment_status: AppointmentPatchStatusSchema,
    db: AsyncSession = Depends(get_session),
    user = Depends(get_current_user)
):
    appointment_service = AppointmentsService(db)
    
    appointment = await appointment_service.patch_appointment_status(appointment_id, new_status=appointment_status, current_user=user)
    
    return appointment


# TODO Criar rota para pegar agenda do veterinário por perído
