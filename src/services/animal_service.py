from typing import List

from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, status, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.animals_schema import (
    AnimalHistorySchema,
    AnimalsSchema,
    AnimalsSchemaTutors,
)
from src.models.__animals_model import AnimalModel
from src.models.__appointments_model import AppointmentsModel

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


class AnimalsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def __validate_animal_weight(self, weight: float):
        if not weight > 0.0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The animal weight must be positive.",
            )

    async def create_animal(self, schema: AnimalsSchemaTutors):
        self.__validate_animal_weight(weight=schema.weight_kg)
        animal: AnimalModel = AnimalModel(**schema.model_dump())

        self.db.add(animal)
        await self.db.commit()

        return animal

    async def get_animals(self) -> List[AnimalModel]:
        async with self.db as session:
            query = select(AnimalModel)
            results = await session.execute(query)

            animals = results.scalars().unique().all()

            return animals

    async def get_animal(self, animal_id: int) -> AnimalModel:
        async with self.db as session:
            query = select(AnimalModel).where(AnimalModel.id == animal_id)
            result = await session.execute(query)

            animal = result.scalars().unique().one_or_none()

            if not animal:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found"
                )

            return animal

    async def put_animal(
        self, animal_id: int, animal: AnimalsSchemaTutors
    ) -> AnimalModel:
        self.__validate_animal_weight(animal.weight_kg)
        async with self.db as session:
            query = select(AnimalModel).filter(AnimalModel.id == animal_id)
            result = await session.execute(query)

            animal_up: AnimalModel = result.scalars().unique().one_or_none()

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
                
    async def delete_animal(
        self, animal_id: int
    ):
        async with self.db as session:
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
                
    async def get_animal_history(self, id):
        stmt = (
            select(AnimalModel)
            .where(AnimalModel.id == id)
            .options(
                selectinload(AnimalModel.appointments)
                .selectinload(AppointmentsModel.medical_record)
            )
        )
        
        result = await self.db.execute(stmt)
        animal = result.scalars().first()
        
        if not animal:
            raise HTTPException(status_code=404, detail="Animal not found")
        
        return animal