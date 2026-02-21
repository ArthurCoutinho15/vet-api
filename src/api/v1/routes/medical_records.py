from typing import List

from fastapi import APIRouter, status, HTTPException, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from src.models.__medical_records_model import MedicalRecordsModel

from src.schemas.medical_records_schema import MedicalRecordSchema

from src.core.configs import settings
from src.core.deps import get_session

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MedicalRecordSchema)
async def post_medical_record(medical_record: MedicalRecordSchema, db: AsyncSession = Depends(get_session)):
    new_medical_record: MedicalRecordsModel = MedicalRecordsModel(
        appointment_id = medical_record.appointment_id,
        vet_id = medical_record.vet_id,
        diagnosis = medical_record.diagnosis,
        treatment = medical_record.treatment,
        prescriptions = [p.model_dump() for p in medical_record.prescriptions] if medical_record.prescriptions else None,
        follow_up_date = medical_record.follow_up_date,
        created_at = medical_record.created_at,
        updated_at = medical_record.updated_at
    )
    
    db.add(new_medical_record)
    await db.commit()
    
    return new_medical_record

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[MedicalRecordSchema])
async def get_medical_records(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MedicalRecordsModel)
        results = await session.execute(query)
        
        medical_records = results.scalars().unique().all()
        
        return medical_records
    
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=MedicalRecordSchema)
async def get_medical_record(medical_record_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MedicalRecordsModel).filter(MedicalRecordsModel.id == medical_record_id)
        result = await session.execute(query)
        
        medical_record = result.scalars().unique().one_or_none()
        
        if not medical_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical Record not found.")
        
        return medical_record
    
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=MedicalRecordSchema)
async def put_medical_record(medical_record_id: int, medical_record: MedicalRecordSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MedicalRecordsModel).filter(MedicalRecordsModel.id == medical_record_id)
        result = await session.execute(query)
        
        medical_record_up: MedicalRecordsModel = result.scalars().unique().one_or_none()
        
        if not medical_record_up:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical Record not found.")
        
        if medical_record:
            if medical_record.appointment_id:
                medical_record_up.appointment_id = medical_record.appointment_id
            if medical_record.vet_id:
                medical_record_up.vet_id = medical_record.vet_id
            if medical_record.diagnosis:
                medical_record_up.diagnosis = medical_record.diagnosis
            if medical_record.treatment:
                medical_record_up.treatment = medical_record.treatment
            if medical_record.prescriptions:
                medical_record_up.prescriptions = [p.model_dump() for p in medical_record.prescriptions]
            if medical_record.follow_up_date:
                medical_record_up.follow_up_date = medical_record.follow_up_date
            if medical_record.created_at:
                medical_record_up.created_at = medical_record.created_at
            if medical_record.updated_at:
                medical_record_up.updated_at = medical_record.updated_at
        
        await session.commit()
        
        return medical_record_up

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medical_record(medical_record_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MedicalRecordsModel).filter(MedicalRecordsModel.id == medical_record_id)
        result = await session.execute(query)
        
        medical_record_del = result.scalars().unique().one_or_none()
        
        if not medical_record_del:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical Record not found.")

        await session.delete(medical_record_del)
        await session.commit()
        
        return Response(content="Medical record deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)

# TODO Exibir prontuários de um animal