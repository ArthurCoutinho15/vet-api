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
from src.services.auth_service import AuthService

from src.core.deps import get_session, get_current_user

router = APIRouter()


@router.get("/me", response_model=UsersBaseSchema)
def get_logged(logged_user: UserModel = Depends(get_current_user)):
    return logged_user

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    auth_service = AuthService(db)
    
    return await auth_service.login(form_data)

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UsersBaseSchema)
async def post_users(user: UserCreateSchema, db: AsyncSession = Depends(get_session), current_user = Depends(get_current_user)):
    auth_service = AuthService(db)
    
    return await auth_service.register_user(user, current_user)
