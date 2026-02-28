from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.tutors_schema import TutorsSchema, TutorWithAnimals, TutorUpdateSchema

from src.services.tutors_service import TutorService

from src.core.deps import get_session, get_current_user

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TutorsSchema)
async def post_tutor(
    tutor: TutorsSchema,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    tutor_service = TutorService(db)

    return await tutor_service.post_tutor(tutor)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[TutorsSchema])
async def get_tutors(
    db: AsyncSession = Depends(get_session), user=Depends(get_current_user)
):
    tutor_service = TutorService(db)

    return await tutor_service.get_tutors()


@router.get("/{tutor_id}", status_code=status.HTTP_200_OK, response_model=TutorsSchema)
async def get_tutor(
    tutor_id: int,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    tutor_service = TutorService(db)

    return await tutor_service.get_tutor(tutor_id)


@router.put(
    "/{tutor_id}",
    response_model=TutorUpdateSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def put_tutor(
    tutor_id: int,
    tutor: TutorUpdateSchema,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    tutor_service = TutorService(db)

    return await tutor_service.put_tutor(tutor_id, tutor)


@router.delete("/{tutor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tutor(
    tutor_id: int,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    tutor_service = TutorService(db)

    return await tutor_service.delete_tutor(tutor_id)


@router.get("/{tutor_id}/animals", response_model=TutorWithAnimals)
async def get_tutor_with_animals(
    tutor_id: int,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):

    tutor_service = TutorService(db)

    return await tutor_service.get_tutor_with_animals(tutor_id)
