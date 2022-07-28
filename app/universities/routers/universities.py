from typing import List, Optional

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from app.auth.crud import get_user
from app.auth.dependencies import Auth
from app.auth.scopes import (
    CREATE_UNIVERSITIES,
    DELETE_UNIVERSITIES,
    EDIT_UNIVERSITIES,
    EDIT_USERS,
    LIST_USERS,
)
from app.db.dependencies import get_db
from app.universities.crud.university import (
    create_university,
    create_university_ownership,
    delete_all_assigned_university,
    delete_university,
    get_assigned_universities,
    is_owner,
    list_universities,
    list_universities_by_slugs,
    update_university,
)
from app.universities.dependencies.universities import (
    get_current_university,
    verify_university_owner,
)
from app.universities.models import University, UniversityOwnership
from app.universities.schemas.universities import (
    UniversityCreate,
    UniversityList,
    UniversityOwnershipRetrieve,
    UniversityRetrieve,
)

router = APIRouter(prefix="/universities")


@router.post(
    "/", response_model=UniversityRetrieve, status_code=status.HTTP_201_CREATED
)
async def create(
    db=Depends(get_db),
    university_in: UniversityCreate = Body(),
    auth: Auth = Security(scopes=[CREATE_UNIVERSITIES]),
):
    university = create_university(db, university_in, auth.user)
    create_university_ownership(db, university.id, auth.user.id)
    return university


@router.get("/", response_model=List[UniversityList])
async def list(
    db=Depends(get_db),
    page: int = Query(1, gt=0),
    page_size: int = Query(100, gt=1, lt=101),
):
    return list_universities(db, page, page_size)


@router.get("/{university_slug}", response_model=UniversityRetrieve)
async def retrieve(university: University = Depends(get_current_university)):
    return university


@router.put(
    "/{university_slug}/",
    response_model=UniversityRetrieve,
    dependencies=[
        Security(verify_university_owner, scopes=[EDIT_UNIVERSITIES])
    ],
)
async def update(
    db=Depends(get_db),
    university: University = Depends(get_current_university),
    university_in: UniversityCreate = Body(),
):
    return update_university(db, university.id, university_in)


@router.delete(
    "/{university_slug}/",
    dependencies=[
        Security(verify_university_owner, scopes=[DELETE_UNIVERSITIES])
    ],
)
async def delete(
    db=Depends(get_db),
    university: University = Depends(get_current_university),
):
    delete_university(db, university.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UNIVERSITY OWNERSHIP
@router.get(
    "/users/{user_id}/ownership",
    dependencies=[Security(Auth, scopes=[LIST_USERS])],
    response_model=UniversityOwnershipRetrieve,
)
async def retrieve_assigned_universities(
    db=Depends(get_db), user_id: int = Path()
):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    universities = get_assigned_universities(db, user_id)

    return UniversityOwnershipRetrieve(
        user=user, university_slugs=[u.slug for u in universities]
    )


@router.put(
    "/users/{user_id}/ownership",
    dependencies=[Security(Auth, scopes=[EDIT_USERS])],
    response_model=UniversityOwnershipRetrieve,
)
async def update_assigned_universities(
    db=Depends(get_db),
    user_id: int = Path(),
    university_slugs: List[str] = Body(embed=True),
):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    delete_all_assigned_university(db, user_id)
    universities = list_universities_by_slugs(db, university_slugs)

    for u in universities:
        if not is_owner(db, u.id, user_id):
            create_university_ownership(db, u.id, user_id)

    return UniversityOwnershipRetrieve(
        user=user, university_slugs=[u.slug for u in universities]
    )
