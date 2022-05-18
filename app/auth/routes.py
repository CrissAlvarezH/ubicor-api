from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.db.dependencies import get_db

from . import schemas
from . import crud
from .utils import authenticate_user, create_access_token

router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=schemas.Token)
async def login(db = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials")

    access_token = create_access_token(
        schemas.TokenData(user_id=user.id, scopes=[s.name for s in user.scopes]))
    return schemas.Token(access_token=access_token)


@router.post("/register", response_model=schemas.Token)
async def register(db = Depends(get_db), user_in: schemas.UserCreate = Body()):
    # check email is not taken
    if crud.get_user(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is taken")

    # if not taken then create user an send email
    user_created = crud.create_user(db, user_in)
    access_token = create_access_token(schemas.TokenData(user_id=user_created.id))

    return schemas.Token(access_token=access_token)
