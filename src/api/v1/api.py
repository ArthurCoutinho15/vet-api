from fastapi import APIRouter

from src.api.v1.routes import tutors, animals, users, appointments, medical_records

api_router = APIRouter()

api_router.include_router(tutors.router, prefix="/tutors", tags=["tutors"])
api_router.include_router(animals.router, prefix="/animals", tags=["animals"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    appointments.router, prefix="/appointments", tags=["appointments"]
)
api_router.include_router(medical_records.router, prefix="/medical-records", tags=["medical records"])
