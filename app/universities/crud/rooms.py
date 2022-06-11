from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.universities.schemas.rooms import RoomCreate
from app.universities.models import Room


def create_room(
    db: Session, building_id: int, room_in: RoomCreate, creator_id: int
) -> Room:
    room = Room(
        **room_in.dict(),
        building_id=building_id,
        created_by=creator_id
    )

    db.add(room)
    db.commit()
    db.refresh(room)

    return room


def search_rooms(db: Session, search: str):
    param = f"%{search}%"
    return (
        db.query(Room)
        .filter(or_(Room.code.ilike(param), Room.name.ilike(param)))
        .all()
    )


def get_room(db: Session, id: int) -> Optional[Room]:
    return (
        db.query(Room)
        .filter(Room.id == id)
        .first()
    )


def update_room(db: Session, id: int, room_in: RoomCreate) -> Room:
    room = get_room(db, id)
    room.name = room_in.name
    room.code = room_in.code
    room.floor = room_in.floor

    db.add(room)
    db.commit()
    db.refresh(room)

    return room


def delete_room(db: Session, id: int):
    room = get_room(db, id)
    db.delete(room)
    db.commit()
