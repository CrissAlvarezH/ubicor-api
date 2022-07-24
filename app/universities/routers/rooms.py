from typing import List

from fastapi import APIRouter, Depends, Query, Security, status, Response, Body

from app.auth.dependencies import Auth
from app.auth.scopes import EDIT_BUILDINGS
from app.db.dependencies import get_db
from app.universities.dependencies.universities import verify_university_owner

from app.universities.models import Building, Room
from app.universities.schemas.rooms import RoomCreate, RoomRetrieve
from app.universities.dependencies.buildings import get_current_building
from app.universities.dependencies.rooms import get_current_room
from app.universities.crud.rooms import create_room, search_rooms, update_room, delete_room


# router for /rooms
standalone_room_router = APIRouter(prefix="/rooms")


@standalone_room_router.get("/", response_model=List[RoomRetrieve])
async def list_standalone(
    db=Depends(get_db),
    search: str = Query(None),
):
    return search_rooms(db, search)


# Router for /university/{university_id}/buildings/{building_id}/rooms
router = APIRouter(prefix="/rooms")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=RoomRetrieve,
    dependencies=[Security(verify_university_owner, scopes=[EDIT_BUILDINGS])]
)
async def create(
    db = Depends(get_db),
    building: Building = Depends(get_current_building),
    room_in: RoomCreate = Body(),
    auth: Auth = Depends()
):
    return create_room(db, building.id, room_in, auth.user.id)


@router.get("/", response_model=List[RoomRetrieve])
async def list(building: Building = Depends(get_current_building)):
    return building.rooms


@router.get("/{room_id}", response_model=RoomRetrieve)
async def retrieve(room: Room = Depends(get_current_room)):
    return room


@router.put(
    "/{room_id}/",
    response_model=RoomRetrieve,
    dependencies=[Security(verify_university_owner, scopes=[EDIT_BUILDINGS])]
)
async def update(
    db = Depends(get_db),
    room: Room = Depends(get_current_room),
    room_in: RoomCreate = Body()
):
    room = update_room(db, room.id, room_in)
    return room


@router.delete(
    "/{room_id}/",
    response_model=RoomRetrieve,
    dependencies=[Security(verify_university_owner, scopes=[EDIT_BUILDINGS])]
)
async def delete(
    db = Depends(get_db),
    room: Room = Depends(get_current_room),
):
    delete_room(db, room.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
