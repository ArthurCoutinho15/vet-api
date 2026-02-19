from fastapi import APIRouter

from src.api.v1.routes import tutors, animals

api_router = APIRouter()

api_router.include_router(tutors.router, prefix='/tutors', tags=["tutors"])
api_router.include_router(animals.router, prefix='/animals', tags=["animals"])
