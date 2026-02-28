from typing import List

from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.animals_schema import (
    AnimalsSchema,
    AnimalsSchemaTutors,
    AnimalHistorySchema,
)

from src.services.animal_service import AnimalsService

from src.core.deps import get_session, get_current_user

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=AnimalsSchemaTutors
)
async def post_animal(
    animal: AnimalsSchemaTutors,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    animal_service = AnimalsService(db)
    new_animal = await animal_service.create_animal(animal)

    return new_animal


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[AnimalsSchema])
async def get_animals(
    db: AsyncSession = Depends(get_session), user=Depends(get_current_user)
):
    animal_service = AnimalsService(db)

    return await animal_service.get_animals()


@router.get(
    "/{animal_id}", status_code=status.HTTP_200_OK, response_model=AnimalsSchema
)
async def get_animal(
    animal_id: int,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    animal_service = AnimalsService(db)

    return await animal_service.get_animal(animal_id)


@router.put(
    "/{animal_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=AnimalsSchemaTutors,
)
async def put_animal(
    animal_id: int,
    animal: AnimalsSchemaTutors,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    animal_service = AnimalsService(db)

    return await animal_service.put_animal(animal_id, animal)


@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_animal(
    animal_id: int,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    animal_service = AnimalsService(db)

    return await animal_service.delete_animal(animal_id)


@router.get(
    "/{id}/history", status_code=status.HTTP_200_OK, response_model=AnimalHistorySchema
)
async def get_animal_history(
    id: int, db: AsyncSession = Depends(get_session), user=Depends(get_current_user)
):

    animal_service = AnimalsService(db)

    return await animal_service.get_animal_history(id)
