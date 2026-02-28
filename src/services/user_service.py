from typing import List, Optional, Any

from fastapi import status, HTTPException, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.models.__user_model import UserModel

from src.schemas.users_schema import (
    UserCreateSchema,
    UsersBaseSchema,
    UserUpdateSchema,
    UserPatchActive,
)

from src.utils.security import security


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _validate_role(self, current_user):
        if current_user.role not in ["admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Admins are allowed for this method.",
            )

    async def get_users(self) -> List[UserModel]:
        query = select(UserModel)
        results = await self.db.execute(query)

        users = results.scalars().unique().all()

        return users

    async def get_user(self, user_id: int) -> UserModel:
        async with self.db as session:
            query = select(UserModel).where(UserModel.id == user_id)
            result = await session.execute(query)

            user = result.scalars().unique().one_or_none()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
                )

            return user

    async def put_user(self, user_id: int, user: UserUpdateSchema) -> UserModel:
        async with self.db as session:
            query = select(UserModel).where(UserModel.id == user_id)
            result = await session.execute(query)

            user_up = result.scalars().unique().one_or_none()

            if not user_up:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
                )

            try:
                if user_up:
                    if user.name:
                        user_up.name = user.name
                    if user.email:
                        user_up.email = user.email
                    if user.password:
                        user_up.password = security.generate_hashed_password(
                            user.password
                        )
                    if user.role:
                        user_up.role = user.role

                    await session.commit()
                    await session.refresh(user_up)

                    return user_up
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This e-mail is already in use.",
                )

    async def delete_user(self, user_id: int):
        async with self.db as session:
            query = select(UserModel).where(UserModel.id == user_id)
            result = await session.execute(query)

            user_del = result.scalars().unique().one_or_none()

            if not user_del:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
                )

            await session.delete(user_del)
            await session.commit()

            return Response(
                status_code=status.HTTP_204_NO_CONTENT,
            )

    async def patch_user_active(
        self, user_id: int, user_active: UserPatchActive, current_user
    ) -> UserModel:
        self._validate_role(current_user)
        async with self.db as session:
            query = select(UserModel).where(UserModel.id == user_id)
            result = await session.execute(query)

            user_patch: UserModel = result.scalars().unique().one_or_none()

            if not user_patch:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
                )

            user_patch.is_active = user_active.is_active
            
            await session.commit()
            await session.refresh(user_patch)

        return user_patch
