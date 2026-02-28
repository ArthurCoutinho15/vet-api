from typing import List

from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.users_schema import (
    UserCreateSchema,
    UsersBaseSchema,
    UserUpdateSchema,
    UserPatchActive,
)

from src.services.user_service import UserService

from src.core.deps import get_session, get_current_user

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UsersBaseSchema])
async def get_users(
    db: AsyncSession = Depends(get_session), user=Depends(get_current_user)
):
    user_service = UserService(db)

    return await user_service.get_users()


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=UsersBaseSchema
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    user_service = UserService(db)

    return await user_service.get_user(user_id)


@router.put(
    "/{user_id}", status_code=status.HTTP_202_ACCEPTED, response_model=UsersBaseSchema
)
async def put_user(
    user_id: int,
    user: UserUpdateSchema,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    user_service = UserService(db)

    return await user_service.put_user(user_id, user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    user_service = UserService(db)

    return await user_service.delete_user(user_id)


@router.patch(
    "/{user_id}", status_code=status.HTTP_202_ACCEPTED, response_model=UsersBaseSchema
)
async def patch_user_is_active(
    user_id: int,
    user_is_active: UserPatchActive,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    user_service = UserService(db)

    return await user_service.patch_user_active(
        user_id, user_is_active, current_user=user
    )
