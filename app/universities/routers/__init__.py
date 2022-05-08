from fastapi import APIRouter

from .universities import router as university_routes
from .buildings import router as building_routes


router = APIRouter()


router.include_router(university_routes)
router.include_router(building_routes)
