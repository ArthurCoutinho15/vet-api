from typing import List, Optional, Any

from fastapi import APIRouter, status, HTTPException, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.models.__tutor_model import TutorModel
from src.models.__animals_model import AnimalModel

from src.schemas.tutors_schema import TutorsSchema, TutorWithAnimals, TutorUpdateSchema
from src.schemas.animals_schema import AnimalsSchemaTutors


class TutorService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def post_tutor(self, tutor: TutorsSchema) -> TutorModel:
        new_tutor = TutorModel(**tutor.model_dump())

        self.db.add(new_tutor)
        await self.db.commit()

        return new_tutor

    async def get_tutors(self) -> List[TutorModel]:
        query = select(TutorModel)
        result = await self.db.execute(query)

        tutors = result.scalars().unique().all()

        return tutors

    async def get_tutor(self, tutor_id: int):
        query = select(TutorModel).where(TutorModel.id == tutor_id)
        result = await self.db.execute(query)

        tutor = result.scalars().unique().one_or_none()

        if not tutor:
            raise HTTPException(
                detail="Tutor not found.", status_code=status.HTTP_404_NOT_FOUND
            )

        return tutor

    async def put_tutor(self, tutor_id: int, tutor: TutorsSchema) -> TutorModel:
        query = select(TutorModel).filter(TutorModel.id == tutor_id)
        result = await self.db.execute(query)

        tutor_up: TutorModel = result.scalars().unique().one_or_none()

        if tutor_up:
            if tutor.name:
                tutor_up.name = tutor.name
            if tutor.cpf:
                tutor_up.cpf = tutor.cpf
            if tutor.email:
                tutor_up.email = tutor.email
            if tutor.phone:
                tutor_up.phone = tutor.phone
            if tutor.address:
                tutor_up.address = tutor.address

            await self.db.commit()

            return tutor_up
        else:
            raise HTTPException(
                detail="Tutor not found.", status_code=status.HTTP_404_NOT_FOUND
            )

    async def delete_tutor(self, tutor_id: int) -> TutorModel:
        query = select(TutorModel).filter(TutorModel.id == tutor_id)
        result = await self.db.execute(query)

        tutor_del: TutorModel = result.scalars().unique().one_or_none()

        if tutor_del:
            await self.db.delete(tutor_del)
            await self.db.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                detail="Tutor not found.", status_code=status.HTTP_404_NOT_FOUND
            )

    async def get_tutor_with_animals(self, tutor_id: int) -> TutorModel:
        query = (
            select(TutorModel)
            .options(selectinload(TutorModel.animals))
            .where(TutorModel.id == tutor_id)
        )

        result = await self.db.execute(query)
        tutor = result.scalars().one_or_none()

        if not tutor:
            raise HTTPException(404, "Tutor not found")

        return tutor
