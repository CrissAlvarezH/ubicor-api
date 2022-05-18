from typing import List

from fastapi import APIRouter, Depends, status, Response, Body

from app.auth.dependencies import Auth
from app.db.dependencies import get_db

from app.universities.models import Building, Room
from app.universities.schemas.rooms import RoomCreate, RoomRetrieve
from app.universities.dependencies.buildings import get_current_building, verify_building_owner
from app.universities.dependencies.rooms import get_current_room
from app.universities.crud.rooms import create_room, update_room, delete_room


router = APIRouter(prefix="/rooms")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=RoomRetrieve
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
    dependencies=[Depends(verify_building_owner)]
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
    dependencies=[Depends(verify_building_owner)]
)
async def delete(
    db = Depends(get_db),
    room: Room = Depends(get_current_room),
):
    delete_room(db, room.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
