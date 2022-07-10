from typing import Optional, Union

from sqlalchemy.orm import Session

from .utils import get_password_hash
from .models import Scope, User
from .schemas import OAuthUserCreate, UserCreate


def get_user(db: Session, user_id: Optional[int] = None,
             email: Optional[str] = None) -> Optional[User]:
    if user_id and email:
        raise ValueError("Only one value must be not null, user id or email.")
    if user_id:
        return db.query(User).filter(User.id == user_id).first()
    if email:
        return db.query(User).filter(User.email == email).first()


def create_user(db: Session, obj_in: Union[UserCreate, OAuthUserCreate]) -> User:
    if isinstance(obj_in, UserCreate):
        provider = "ubicor"
        password = get_password_hash(obj_in.password)
    elif isinstance(obj_in, OAuthUserCreate):
        provider = obj_in.provider
        password = "@"

    db_obj = User(
        full_name=obj_in.full_name,
        email=obj_in.email,
        password=password,
        provider=provider
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_scope(db: Session, scope_name: str) -> Scope:
    scope = Scope(name=scope_name)
    db.add(scope)
    db.commit()
    db.refresh(scope)
    return scope
