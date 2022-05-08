from typing import Optional

from sqlalchemy.orm import Session

from app.universities.schemas.positions import PositionCreate
from app.universities.models import Position


def get_position(db: Session, id: int) -> Optional[Position]:
    return db.query(Position).get(id)


def create_position(db: Session, position_in: PositionCreate) -> Position:
    position = Position(**position_in.dict())
    db.add(position)
    db.commit()
    db.refresh(position)
    return position


def update_position(db: Session, id: int, position_in: PositionCreate) -> Position:
    position = get_position(db, id)
    for key, value in position_in.dict().items():
        position.__setattr__(key, value)
    db.add(position)
    db.commit()
    db.refresh(position)
    return position
