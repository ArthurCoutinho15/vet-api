from typing import List, Optional, Any

from fastapi import APIRouter, status, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.models.__user_model import UserModel

from src.schemas.users_schema import UserCreateSchema, UsersBaseSchema

from src.utils.security import security
from src.utils.auth import authenticate_user, _create_access_token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
        
    def __validate_role(self, current_user):
        if current_user.role not in ["admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to create users",
            ) 
            
    async def login(self, form_data):
        user = await authenticate_user(email=form_data.username, password=form_data.password, db=self.db)
        
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dados de acesso incorretos.")
        
        return JSONResponse(
            content={
                "access_token": _create_access_token(sub=user.id),
                "token_type": "bearer"
            },
            status_code=status.HTTP_200_OK
        )
            
    async def register_user(self, user: UserCreateSchema, current_user):
        
        self.__validate_role(current_user)
        new_user = UserModel(
            name=user.name,
            email=user.email,
            password=security.generate_hashed_password(user.password),
            role=user.role,
        )

        try:
            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)
            return new_user

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This e-mail is already in use.",
            )
