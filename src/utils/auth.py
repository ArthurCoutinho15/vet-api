from pytz import timezone
from datetime import timedelta, datetime
from typing import Optional, List

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import EmailStr

from jose import jwt

from src.models.__user_model import UserModel
from src.core.configs import settings
from src.utils.security import security

oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/usuarios/login")


async def authenticate_user(
    email: EmailStr, password: str, db: AsyncSession
) -> Optional[UserModel]:
    async with db as session:
        query = select(UserModel).filter(UserModel.email == email)
        result = await session.execute(query)

        user: UserModel = result.scalars().one_or_none()

        if not user:
            return None
        if not security.verify_password(password, user.password):
            return None

        return user


def __create_token(token_type: str, lifetime: timedelta, sub: str) -> str:
    payload = {}
    sp = timezone("America/Sao_Paulo")
    expires = datetime.now(tz=sp) + lifetime

    payload["type"] = token_type
    payload["exp"] = expires
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def __create_access_token(sub: str) -> str:
    return __create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )
