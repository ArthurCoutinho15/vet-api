from typing import List

from fastapi import APIRouter, status, HTTPException, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from src.models.__medical_records_model import MedicalRecordsModel

from src.schemas.medical_records_schema import (
    MedicalRecordSchema,
    MedicalRecordCreateSchema,
    MedicalRecordUpdateSchema,
)

from src.services.medical_records_service import MedicalRecordsService
from src.core.configs import settings
from src.core.deps import get_session, get_current_user

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=MedicalRecordSchema
)
async def post_medical_record(
    medical_record: MedicalRecordCreateSchema,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    medical_record_service = MedicalRecordsService(db)

    return await medical_record_service.post_medical_records(medical_record, user)


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[MedicalRecordSchema]
)
async def get_medical_records(
    db: AsyncSession = Depends(get_session), user=Depends(get_current_user)
):
    medical_record_service = MedicalRecordsService(db)

    return await medical_record_service.get_medical_records()


@router.get(
    "/{medical_record_id}",
    status_code=status.HTTP_200_OK,
    response_model=MedicalRecordSchema,
)
async def get_medical_record(
    medical_record_id: int,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    medical_record_service = MedicalRecordsService(db)

    return await medical_record_service.get_medical_record(medical_record_id)


@router.put(
    "/{medical_record_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=MedicalRecordSchema,
)
async def put_medical_record(
    medical_record_id: int,
    medical_record: MedicalRecordUpdateSchema,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    medical_record_service = MedicalRecordsService(db)

    return await medical_record_service.put_medical_record(
        medical_record_id, medical_record, user
    )


@router.delete("/{medical_record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medical_record(
    medical_record_id: int,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    medical_record_service = MedicalRecordsService(db)

    return await medical_record_service.delete_medical_record(medical_record_id)


# TODO Exibir prontuários de um animal
