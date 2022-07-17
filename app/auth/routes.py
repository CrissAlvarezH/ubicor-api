from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.db.dependencies import get_db

from . import schemas
from . import crud
from .utils import authenticate_user, create_access_token

router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=schemas.Token)
async def login(db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials")

    access_token = create_access_token(
        schemas.TokenData(user_id=user.id, scopes=[s.name for s in user.scopes]))
    return schemas.Token(user=user, access_token=access_token)


@router.post("/register", response_model=schemas.Token)
async def register(db=Depends(get_db), user_in: schemas.UserCreate = Body()):
    # check email is not taken
    if crud.get_user(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is taken")

    # if not taken then create user an send email
    user_created = crud.create_user(db, user_in)
    access_token = create_access_token(schemas.TokenData(user_id=user_created.id))

    return schemas.Token(user=user_created, access_token=access_token)


@router.post("/get-or-create-user", response_model=schemas.UserRetrieve)
async def getOrCreateUser(db=Depends(get_db), user_in: schemas.OAuthUserCreate = Body()):
    # check email is not taken
    user = crud.get_user(db, email=user_in.email)
    if user:
        return user

    if user_in.full_name is None or user_in.provider is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "full_name and provider required")

    user = crud.create_user(db, user_in)
    return user
