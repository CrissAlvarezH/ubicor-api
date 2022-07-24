from fastapi import Depends, Path, status, HTTPException

from app.auth.dependencies import Auth
from app.db.dependencies import get_db

from app.universities.models import University
from app.universities.crud.university import get_university_by_slug, is_owner


async def get_current_university(
    db=Depends(get_db),
    university_slug: str = Path()
) -> University:
    university = get_university_by_slug(db, university_slug)
    if not university:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="University not found"
        )
    return university


async def verify_university_owner(
    db=Depends(get_db),
    university: University = Depends(get_current_university),
    auth: Auth = Depends()
):
    if not is_owner(db, university.id, auth.user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You dont have ownership with this university"
        )
