from typing import List, Optional, Any

from fastapi import APIRouter, status, HTTPException, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.models.__tutor_model import TutorModel
from src.models.__animals_model import AnimalModel

from src.schemas.tutors_schema import TutorsSchema, TutorWithAnimals
from src.schemas.animals_schema import AnimalsSchemaTutors

from src.core.deps import get_session

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TutorsSchema)
async def post_tutor(tutor: TutorsSchema, db: AsyncSession = Depends(get_session)):

    new_tutor: TutorModel = TutorModel(
        name=tutor.name,
        cpf=tutor.cpf,
        email=tutor.email,
        phone=tutor.phone,
        address=tutor.address,
    )

    db.add(new_tutor)

    await db.commit()

    return new_tutor


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[TutorsSchema])
async def get_tutors(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TutorModel)
        result = await session.execute(query)

        tutors: List[TutorModel] = result.scalars().unique().all()

        return tutors


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=TutorsSchema)
async def get_tutor(tutor_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TutorModel).filter(TutorModel.id == tutor_id)
        result = await session.execute(query)

        tutor: TutorModel = result.scalars().unique().one_or_none()

        if tutor:
            return tutor
        else:
            raise HTTPException(
                detail="Tutor not found.", status_code=status.HTTP_404_NOT_FOUND
            )


@router.put("/{id}", response_model=TutorsSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_tutor(
    tutor_id: int, tutor: TutorsSchema, db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(TutorModel).filter(TutorModel.id == tutor_id)
        result = await session.execute(query)

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
                
            await session.commit()
            
            return tutor_up
        else:
            raise HTTPException(
                detail="Tutor not found.", status_code=status.HTTP_404_NOT_FOUND
            )

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tutor(tutor_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TutorModel).filter(TutorModel.id == tutor_id)
        result = await session.execute(query)
        
        tutor_del: TutorModel = result.scalars().unique().one_or_none()
        
        if tutor_del:
            await session.delete(tutor_del)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Tutor not found.", status_code=status.HTTP_404_NOT_FOUND)
             

@router.get("/{id}/animals", response_model=TutorWithAnimals)
async def get_tutor_with_animals(
    tutor_id: int,
    db: AsyncSession = Depends(get_session)
):
    query = (
        select(TutorModel)
        .options(selectinload(TutorModel.animals))
        .where(TutorModel.id == tutor_id)
    )

    result = await db.execute(query)
    tutor = result.scalars().one_or_none()

    if not tutor:
        raise HTTPException(404, "Tutor not found")

    return tutor