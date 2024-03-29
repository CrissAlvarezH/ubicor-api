from fastapi import APIRouter

from .building_zones import router as building_zone_router
from .buildings import router as building_routes
from .reports import router as report_routes
from .rooms import router as room_routes
from .rooms import standalone_room_router
from .universities import router as university_routes

router = APIRouter()


router.include_router(university_routes, tags=["University"])
router.include_router(
    building_routes,
    tags=["Buildings"],
    prefix="/universities/{university_slug}",
)
router.include_router(
    room_routes,
    tags=["Rooms"],
    prefix="/universities/{university_slug}/buildings/{building_id}",
)
router.include_router(standalone_room_router, tags=["Rooms"])
router.include_router(
    building_zone_router,
    tags=["building-zones"],
    prefix="/universities/{university_slug}",
)
router.include_router(report_routes, tags=["Reports"], prefix="/reports")
