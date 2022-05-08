from fastapi import APIRouter

from .universities import router as university_routes
from .buildings import router as building_routes
from .rooms import router as room_routes


router = APIRouter()


router.include_router(university_routes, tags=["University"])
router.include_router(building_routes, tags=["Buildings"], prefix="/universities/{university_id}")
router.include_router(room_routes, tags=["Rooms"], prefix="/universities/{university_id}/buildings/{building_id}")
