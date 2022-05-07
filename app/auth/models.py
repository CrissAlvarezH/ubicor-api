from sqlalchemy import Column, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    scopes = relationship(
        "Scope",
        primaryjoin="UserScope.user_id == User.id",
        secondary="join(Scope, UserScope, UserScope.scope_name == Scope.name)",
        viewonly=True
    )


class Scope(Base):
    __tablename__ = "scopes"

    name = Column(String, primary_key=True)


class UserScope(Base):
    __tablename__ = "users_scopes"

    user_id = Column(ForeignKey("users.id"), primary_key=True)
    scope_name = Column(ForeignKey("scopes.name"), primary_key=True)
