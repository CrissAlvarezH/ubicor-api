from fastapi import Depends, Path, status, HTTPException, Request

from app.auth.dependencies import Auth
from app.db.dependencies import get_db

from app.universities.models import University
from app.universities.crud.university import get_university



async def get_current_university(
    db = Depends(get_db),
    university_id: int = Path(gt=0)
) -> University:
    university = get_university(db, university_id)
    if not university:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="University not found"
        )
    return university

async def verify_university_owner(
    university: University = Depends(get_current_university),
    auth: Auth = Depends()    
):
    if auth.user.id != university.created_by and not auth.user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to perform this action"
        )