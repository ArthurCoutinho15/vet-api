from typing import List, Optional, Any

from fastapi import APIRouter, status, HTTPException, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.models.__user_model import UserModel

from src.schemas.users_schema import UserCreateSchema, UsersBaseSchema

from src.core.deps import get_session
from src.utils.security import security

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UsersBaseSchema)
async def post_users(user: UserCreateSchema, db: AsyncSession = Depends(get_session)):

    new_user = UserModel(
        name=user.name,
        email=user.email,
        password=security.generate_hashed_password(user.password),
        role=user.role,
    )

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This e-mail is already in use.",
        )


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UsersBaseSchema])
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)

        users: List[UserModel] = result.scalars().unique().all()

        return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UsersBaseSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)

        user: UserModel = result.scalars().unique().one_or_none()

        if user:
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )


@router.put(
    "/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=UsersBaseSchema
)
async def put_user(
    user_id: int, user: UserCreateSchema, db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)

        user_up: UserModel = result.scalars().unique().one_or_none()

        if user_up:
            if user.name:
                user_up.name = user.name
            if user.email:
                user_up.email = user.email
            if user.password:
                user_up.password = security.generate_hashed_password(user.password)
            if user.role:
                user_up.role = user.role

            await session.commit()

            return user_up
        else:
            raise HTTPException(
                status_code=status.HTTP_404_BAD_REQUEST, detail="User not found."
            )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)

        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_BAD_REQUEST, detail="User not found."
            )

        await session.delete(user)
        await session.commit()

        return Response(
            content="User deleted successfully", status_code=status.HTTP_204_NO_CONTENT
        )


# TODO
# Rota patch para admins desativarem usuários
