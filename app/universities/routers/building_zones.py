from typing import List

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
    Response,
    Security,
    status,
)
from sqlalchemy.exc import IntegrityError

from app.auth import dependencies
from app.auth.dependencies import Auth
from app.auth.scopes import CREATE_BUILDINGS, EDIT_UNIVERSITIES
from app.db.dependencies import get_db
from app.universities.crud.buildings import (
    create_building_zone,
    delete_building_zone,
    get_building_zone,
    list_building_zones,
)
from app.universities.dependencies.universities import verify_university_owner
from app.universities.schemas.buildings import (
    BuildingZoneCreate,
    BuildingZoneRetrieve,
)

router = APIRouter(prefix="/building-zones")


@router.get(
    "",
    response_model=List[BuildingZoneRetrieve],
    dependencies=[
        Security(verify_university_owner, scopes=[EDIT_UNIVERSITIES])
    ],
)
async def list(db=Depends(get_db), university_slug: str = Path()):
    return list_building_zones(db, university_slug)


@router.post(
    "/",
    response_model=BuildingZoneRetrieve,
    dependencies=[
        Security(verify_university_owner, scopes=[EDIT_UNIVERSITIES])
    ],
)
async def create(
    db=Depends(get_db), building_zone_in: BuildingZoneCreate = Body()
):
    try:
        building_zone = get_building_zone(db, **building_zone_in.dict())
        if building_zone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This zone already exist",
            )
        return create_building_zone(db, **building_zone_in.dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.delete(
    "/{building_zone_id}/",
    dependencies=[
        Security(verify_university_owner, scopes=[EDIT_UNIVERSITIES])
    ],
)
async def delete(db=Depends(get_db), building_zone_id: int = Path()):
    try:
        delete_building_zone(db, building_zone_id)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="this zone is been used",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
