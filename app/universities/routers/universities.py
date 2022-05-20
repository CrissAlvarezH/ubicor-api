from typing import List

from fastapi import APIRouter, Body, Depends, \
    Query, Response, status

from app.db.dependencies import get_db
from app.auth.dependencies import Auth

from app.universities.crud.university import create_university, \
    list_universities, update_university, delete_university
from app.universities.dependencies.universities import get_current_university, \
    verify_university_owner
from app.universities.models import University
from app.universities.schemas.universities import UniversityCreate, \
    UniversityRetrieve


router = APIRouter(prefix="/universities")


@router.post(
    "/",
    response_model=UniversityRetrieve,
    status_code=status.HTTP_201_CREATED
)
async def create(
    db=Depends(get_db),
    university_in: UniversityCreate = Body(),
    auth: Auth = Depends()
):
    university = create_university(db, university_in, auth.user)
    return university


@router.get("/", response_model=List[UniversityRetrieve])
async def list(
    db=Depends(get_db),
    page: int = Query(1, gt=0),
    page_size: int = Query(100, gt=1, lt=101)
):
    return list_universities(db, page, page_size)


@router.get("/{university_slug}", response_model=UniversityRetrieve)
async def retrieve(
    university: University = Depends(get_current_university)
):
    return university


@router.put(
    "/{university_slug}/",
    response_model=UniversityRetrieve,
    dependencies=[Depends(verify_university_owner)]
)
async def update(
    db=Depends(get_db),
    university: University = Depends(get_current_university),
    university_in: UniversityCreate = Body(),
):
    return update_university(db, university.id, university_in)


@router.delete(
    "/{university_slug}/",
    dependencies=[Depends(verify_university_owner)]
)
async def delete(
    db=Depends(get_db),
    university: University = Depends(get_current_university),
):
    delete_university(db, university.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
