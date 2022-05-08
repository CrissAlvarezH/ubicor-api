import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from pydantic import ValidationError

from app.core.config import settings
from app.db.dependencies import get_db

from . import crud
from . import models


LOG = logging.getLogger("auth.dependencies")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    db = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception

        user = crud.get_user(db, user_id=user_id)

        if user is None:
            raise credentials_exception
    except (JWTError, ValidationError) as e:
        LOG.error(f"Error on get_current_user: {str(e)}")
        LOG.exception(e)
        raise credentials_exception
    
    return user


async def get_current_active_user(current_user = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class Auth:
    user: models.User

    def __init__(self, user = Depends(get_current_active_user)):
        self.user = user
