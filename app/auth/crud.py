from typing import Optional, Union, List

from sqlalchemy.orm import Session

from .utils import get_password_hash
from .models import Scope, User, UserScope
from .schemas import OAuthUserCreate, UserCreate, UserUpdate


def get_user(db: Session, user_id: Optional[int] = None,
             email: Optional[str] = None) -> Optional[User]:
    if user_id and email:
        raise ValueError("Only one value must be not null, user id or email.")
    if user_id:
        return db.query(User).filter(User.id == user_id).first()
    if email:
        return db.query(User).filter(User.email == email).first()


def list_users(db: Session) -> List[User]:
    return db.query(User).all()


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


def add_scope_to_user(db: Session, user_id: int, scope: str):
    if not get_scope(db, scope):
        raise ValueError("scope does't exists")
    user_scope = UserScope(user_id=user_id, scope_name=scope)
    db.add(user_scope)
    db.commit()


def remove_all_scopes(db: Session, user_id: int):
    db.query(UserScope).filter(UserScope.user_id == user_id).delete()
    db.commit()


def update_user(db: Session, user_id: int, obj_in: UserUpdate) -> User:
    user = get_user(db, user_id=user_id)
    if not user:
        raise ValueError("dons't exist user")

    if obj_in.full_name:
        user.full_name = obj_in.full_name
    if obj_in.scopes:
        remove_all_scopes(db, user_id)
        for scope in obj_in.scopes:
            add_scope_to_user(db, user_id, scope)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_scope(db: Session, scope_name: str) -> Optional[Scope]:
    return db.query(Scope).filter(Scope.name == scope_name).first()


def create_scope(db: Session, scope_name: str) -> Scope:
    scope = Scope(name=scope_name)
    db.add(scope)
    db.commit()
    db.refresh(scope)
    return scope


def list_scopes(db: Session) -> List[Scope]:
    return db.query(Scope).all()
