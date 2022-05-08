from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, \
    Boolean, ForeignKey, Float

from app.db.base_class import Base


class TimestampsMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)


class University(Base, TimestampsMixin):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True)
    is_active = Column(Boolean, default=False)
    created_by = Column(ForeignKey("users.id"))
    position_id = Column(ForeignKey("positions.id"))

    position = relationship("Position")


class Building(Base, TimestampsMixin):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String, index=True)
    created_by = Column(ForeignKey("users.id"))
    position_id = Column(ForeignKey("positions.id"))
    university_id = Column(ForeignKey("universities.id"))


class Room(Base, TimestampsMixin):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    floor = Column(Integer)
    created_by = Column(ForeignKey("users.id"))
    building_id = Column(ForeignKey("buildings.id"))
 