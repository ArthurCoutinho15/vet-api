from typing import List

from fastapi import APIRouter, status, HTTPException, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from src.models.__tutor_model import TutorModel
from src.models.__animals_model import AnimalModel

from src.schemas.tutors_schema import TutorsSchema
from src.schemas.animals_schema import AnimalsSchema, AnimalsSchemaTutors

from src.core.deps import get_session

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=AnimalsSchemaTutors
)
async def post_animal(
    animal: AnimalsSchemaTutors, db: AsyncSession = Depends(get_session)
):
    new_animal: AnimalModel = AnimalModel(
        name=animal.name,
        species=animal.species,
        breed=animal.breed,
        birth_date=animal.birth_date,
        weight_kg=animal.weight_kg,
        tutor_id=animal.tutor_id,
    )

    db.add(new_animal)
    await db.commit()

    return new_animal


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[AnimalsSchema])
async def get_animals(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AnimalModel)
        result = await session.execute(query)

        animals: List[AnimalModel] = result.scalars().unique().all()

        return animals


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=AnimalsSchema)
async def get_animal(animal_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AnimalModel).filter(AnimalModel.id == animal_id)
        result = await session.execute(query)

        animal = result.scalars().unique().one_or_none()

        if not animal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found"
            )

        return animal


@router.put(
    "/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=AnimalsSchemaTutors
)
async def put_animal(
    animal_id: int, animal: AnimalsSchemaTutors, db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(AnimalModel).filter(AnimalModel.id == animal_id)
        result = await session.execute(query)

        animal_up: AnimalsSchemaTutors = result.scalars().unique().one_or_none()

        if animal_up:
            if animal.name:
                animal_up.name = animal.name
            if animal.species:
                animal_up.species = animal.species
            if animal.breed:
                animal_up.breed = animal.breed
            if animal.birth_date:
                animal_up.birth_date = animal.birth_date
            if animal.weight_kg:
                animal_up.weight_kg = animal.weight_kg
            if animal.tutor_id:
                animal_up.tutor_id = animal.tutor_id

            await session.commit()
            return animal_up

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found"
            )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_animal(animal_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AnimalModel).filter(AnimalModel.id == animal_id)
        result = await session.execute(query)

        animal_del: AnimalModel = result.scalars().unique().one_or_none()

        if animal_del:
            await session.delete(animal_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found"
            )


# TODO Histórico médico do animal
