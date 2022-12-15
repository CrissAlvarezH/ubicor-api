from typing import List

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
    Security,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from google.auth.transport import requests
from google.oauth2 import id_token

from app.auth.dependencies import Auth
from app.auth.scopes import EDIT_USERS, LIST_USERS
from app.core.config import settings
from app.db.dependencies import get_db

from . import crud, schemas
from .utils import authenticate_user, create_access_token

router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=schemas.Token)
async def login(
    db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials",
        )

    access_token = create_access_token(
        schemas.TokenData(user=user)
    )
    return schemas.Token(access_token=access_token)


@router.post("/register", response_model=schemas.Token)
async def register(db=Depends(get_db), user_in: schemas.UserCreate = Body()):
    # check email is not taken
    if crud.get_user(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is taken"
        )

    # if not taken then create user an send email
    user_created = crud.create_user(db, user_in)
    access_token = create_access_token(
        schemas.TokenData(user=user_created)
    )

    return schemas.Token(access_token=access_token)


@router.post("/token-sign-in", response_model=schemas.Token)
async def token_sign_in(
    db=Depends(get_db), token_id: str = Body(), provider: str = Body()
):
    if provider == "google":
        try:
            idinfo = id_token.verify_oauth2_token(
                token_id, requests.Request(), settings.GOOGLE_CLIENT_ID
            )

            # get user or create if not exits
            user = crud.get_user(db, email=idinfo.get("email"))
            if not user:
                user_data = schemas.OAuthUserCreate(
                    full_name=idinfo.get("name"),
                    email=idinfo.get("email"),
                    provider="google",
                )
                user = crud.create_user(db, user_data)

            access_token = create_access_token(
                schemas.TokenData(user=user)
            )
            return schemas.Token(access_token=access_token)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="invalid token"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="provider not supported",
        )


# USERS
@router.get(
    "/users",
    response_model=List[schemas.UserRetrieve],
    dependencies=[Security(Auth, scopes=[LIST_USERS])],
)
async def user_list(db=Depends(get_db)):
    return crud.list_users(db)


@router.put(
    "/users/{user_id}/",
    response_model=schemas.UserRetrieve,
    dependencies=[Security(Auth, scopes=[EDIT_USERS])],
)
async def user_edit(
    db=Depends(get_db),
    user_id: int = Path(),
    user_in: schemas.UserUpdate = Body(),
):
    try:
        user = crud.update_user(db, user_id, user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
