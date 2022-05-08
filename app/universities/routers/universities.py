from typing import List

from fastapi import APIRouter, Body, Depends, Path, \
    HTTPException, Query, Response, status

from app.db.dependencies import get_db
from app.auth.dependencies import Auth

from app.universities.crud.university import create_university, \
    get_university, list_universities, update_university, delete_university
from app.universities.schemas.universities import UniversityCreate, \
    UniversityRetrieve


router = APIRouter()


@router.post("/", response_model=UniversityRetrieve)
async def create(
    db = Depends(get_db),
    university_in: UniversityCreate = Body(...),
    auth: Auth = Depends()
):
    university = create_university(db, university_in, auth.user)
    return university


@router.get("/", response_model=List[UniversityRetrieve])
async def list(
    db = Depends(get_db),
    page: int = Query(1, gt=0),
    page_size: int = Query(100, gt=1, lt=101)
):
    return list_universities(db, page, page_size)


@router.get("/{id}", response_model=UniversityRetrieve)
async def retrieve(
    db = Depends(get_db),
    id: int = Path(..., gt=0)
):
    university = get_university(db, id)    
    if not university:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return university


@router.put("/{id}/", response_model=UniversityRetrieve)
async def update(
    db = Depends(get_db),
    id: int = Path(..., gt=0),
    university_in: UniversityCreate = Body(...),
    auth: Auth = Depends()
):
    university = get_university(db, id)
    if not university:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Validate if current user is the creator or superuser
    if university.created_by != auth.user.id and not auth.user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return update_university(db, id, university_in)


@router.delete("/{id}/")
async def delete(
    db = Depends(get_db),
    id: int = Path(..., gt=0),
    auth: Auth = Depends()
):
    university = get_university(db, id)
    if not university:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Validate if current user is the creator or superuser
    if university.created_by != auth.user.id and not auth.user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    delete_university(db, id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
