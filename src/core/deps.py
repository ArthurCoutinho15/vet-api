from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import Session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()
