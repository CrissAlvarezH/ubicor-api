from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.auth.dependencies import Auth
from app.db.dependencies import get_db
from app.universities.crud.buildings import get_building
from app.universities.models import Building


async def get_current_building(
    db: Session = Depends(get_db), building_id: int = Path(gt=0)
) -> Building:
    building = get_building(db, building_id)
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Building not found"
        )
    return building
