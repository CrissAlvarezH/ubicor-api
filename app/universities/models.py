from datetime import datetime
from email.policy import default

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
    buildings = relationship("Building")


class Building(Base, TimestampsMixin):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String, index=True)
    is_active = Column(Boolean, default=False)
    created_by = Column(ForeignKey("users.id"))
    position_id = Column(ForeignKey("positions.id"))
    university_id = Column(ForeignKey("universities.id"))

    creator = relationship("User")
    position = relationship("Position")
    rooms = relationship("Room")
    building_images = relationship("BuildingImage")
    images = relationship(
        "Image",
        secondary="join(BuildingImage, Image, BuildingImage.image_id == Image.id)",
        primaryjoin="BuildingImage.building_id == Building.id",
        viewonly=True
    )


class BuildingImage(Base):
    __tablename__ = "buildings_images"

    building_id = Column(ForeignKey("buildings.id"), primary_key=True)
    image_id = Column(ForeignKey("images.id"), primary_key=True)
    priority_order = Column(Integer, default=1)

    image = relationship("Image")


class Image(Base, TimestampsMixin):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    small = Column(String)
    medium = Column(String)
    original = Column(String)


class Room(Base, TimestampsMixin):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    floor = Column(Integer)
    created_by = Column(ForeignKey("users.id"))
    building_id = Column(ForeignKey("buildings.id"))

    creator = relationship("User")
 