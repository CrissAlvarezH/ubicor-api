from fastapi import Depends, Path, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import Auth

from app.db.dependencies import get_db

from app.universities.models import Building
from app.universities.crud.buildings import get_building


async def get_current_building(
    db: Session = Depends(get_db),
    building_id: int = Path(gt=0)
) -> Building:
    building = get_building(db, building_id)
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    return building


async def verify_building_owner(
    building: Building = Depends(get_current_building),
    auth: Auth = Depends()
):
    if building.created_by != auth.user.id and not auth.user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permissions to perform this action"
        )
