from typing import List

from fastapi import APIRouter, Body, Depends, Response, status

from app.auth.dependencies import Auth

from app.db.dependencies import get_db
from app.universities.dependencies.buildings import get_current_building, verify_building_owner
from app.universities.dependencies.universities import get_current_university, \
    verify_university_owner
from app.universities.models import University, Building

from app.universities.schemas.buildings import BuildingCreate, \
    BuildingRetrieve
from app.universities.crud.buildings import create_building, delete_building, update_building
from app.universities.crud.university import get_university


router = APIRouter(prefix="/buildings")


@router.post(
    "/",
    response_model=BuildingRetrieve,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_university_owner)]
)
def create(
    db = Depends(get_db),
    university: University = Depends(get_current_university),
    building_in: BuildingCreate = Body(...),
    auth: Auth = Depends()
):
    return create_building(db, university.id, building_in, auth.user)


@router.get("/", response_model=List[BuildingRetrieve])
def list(university: University = Depends(get_current_university)):
    return university.buildings


@router.get("/{building_id}", response_model=BuildingRetrieve)
def retrieve(building: Building = Depends(get_current_building)):
    return building


@router.put(
    "/{building_id}/",
    response_model=BuildingRetrieve,
    dependencies=[Depends(verify_building_owner)]
)
def update(
    db = Depends(get_db),
    building: Building = Depends(get_current_building),
    building_in: BuildingCreate = Body(...)
):
    return update_building(db, building.id, building_in)


@router.delete(
    "/{building_id}/", dependencies=[Depends(verify_building_owner)])
def delete(
    db = Depends(get_db),
    building: Building = Depends(get_current_building)
):
    delete_building(db, building.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    