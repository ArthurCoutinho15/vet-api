from typing import List

from fastapi import status, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.__medical_records_model import MedicalRecordsModel
from src.models.__user_model import UserModel
from src.models.__appointments_model import AppointmentsModel

from src.schemas.medical_records_schema import (
    MedicalRecordSchema,
    MedicalRecordCreateSchema,
    MedicalRecordUpdateSchema,
)

class MedicalRecordsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def __validate_vet(self, current_user: UserModel, appointment_id: int):
        query = select(AppointmentsModel.vet_id).where(
            AppointmentsModel.id == appointment_id
        )

        result = await self.db.execute(query)
        vet_id = result.scalar_one_or_none()

        if not vet_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
            )

        if current_user.id != vet_id:
            raise HTTPException(
                status_code=403,
                detail="You are not the veterinarian of this appointment.",
            )

    async def post_medical_records(
        self, medical_record: MedicalRecordCreateSchema, user: UserModel
    ) -> MedicalRecordsModel:
        await self.__validate_vet(
            current_user=user, appointment_id=medical_record.appointment_id
        )

        new_medical_record: MedicalRecordsModel = MedicalRecordsModel(
            appointment_id=medical_record.appointment_id,
            vet_id=user.id,
            diagnosis=medical_record.diagnosis,
            treatment=medical_record.treatment,
            prescriptions=[p.model_dump() for p in medical_record.prescriptions]
            if medical_record.prescriptions
            else None,
            follow_up_date=medical_record.follow_up_date,
            created_at=medical_record.created_at,
            updated_at=medical_record.updated_at,
        )

        self.db.add(new_medical_record)
        await self.db.commit()
        await self.db.refresh(new_medical_record)

        return new_medical_record

    async def get_medical_records(self) -> List[MedicalRecordsModel]:
        query = select(MedicalRecordsModel)
        result = await self.db.execute(query)

        medical_records = result.scalars().unique().all()

        return medical_records

    async def get_medical_record(self, medical_record_id: int) -> MedicalRecordsModel:
        query = select(MedicalRecordsModel).filter(
            MedicalRecordsModel.id == medical_record_id
        )
        result = await self.db.execute(query)

        medical_record = result.scalars().unique().one_or_none()

        if not medical_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical Record not found.",
            )

        return medical_record

    async def put_medical_record(
        self,
        medical_record_id: int,
        medical_record: MedicalRecordUpdateSchema,
        current_user=UserModel,
    ) -> MedicalRecordsModel:

        self.__validate_vet(current_user, medical_record.appointment_id)
        query = select(MedicalRecordsModel).filter(
            MedicalRecordsModel.id == medical_record_id
        )
        result = await self.db.execute(query)

        medical_record_up: MedicalRecordsModel = result.scalars().unique().one_or_none()

        if not medical_record_up:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical Record not found.",
            )

        if medical_record:
            if medical_record.appointment_id:
                medical_record_up.appointment_id = medical_record.appointment_id
            if medical_record.vet_id:
                medical_record_up.vet_id = current_user.id
            if medical_record.diagnosis:
                medical_record_up.diagnosis = medical_record.diagnosis
            if medical_record.treatment:
                medical_record_up.treatment = medical_record.treatment
            if medical_record.prescriptions:
                medical_record_up.prescriptions = [
                    p.model_dump() for p in medical_record.prescriptions
                ]
            if medical_record.follow_up_date:
                medical_record_up.follow_up_date = medical_record.follow_up_date
            if medical_record.created_at:
                medical_record_up.created_at = medical_record.created_at
            if medical_record.updated_at:
                medical_record_up.updated_at = medical_record.updated_at

        await self.db.commit()
        await self.db.refresh(medical_record_up)

        return medical_record_up

    async def delete_medical_record(self, medical_record_id: int):
        query = select(MedicalRecordsModel).where(
            MedicalRecordsModel.id == medical_record_id
        )
        result = await self.db.execute(query)

        medical_record_del = result.scalar_one_or_none()

        if not medical_record_del:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical Record not found.",
            )

        await self.db.delete(medical_record_del)
        await self.db.commit()

        return Response(
            content="Medical record deleted successfully.",
            status_code=status.HTTP_204_NO_CONTENT,
        )
