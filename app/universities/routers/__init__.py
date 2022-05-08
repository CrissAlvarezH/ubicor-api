from fastapi import APIRouter

from .universities import router as university_routes

router = APIRouter()

router.include_router(university_routes, prefix="/university")