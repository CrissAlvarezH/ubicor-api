from fastapi import Depends, HTTPException, Path, status

from app.db.dependencies import get_db
from app.universities.crud.rooms import get_room
from app.universities.models import Room


async def get_current_room(
    db=Depends(get_db), room_id: int = Path(gt=0)
) -> Room:
    room = get_room(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )
    return room
