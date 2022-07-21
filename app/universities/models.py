from datetime import datetime

from sqlalchemy.orm import relationship, object_session
from sqlalchemy import Column, Integer, String, DateTime, \
    Boolean, ForeignKey, Float

from app.db.base_class import Base


class TimestampsMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float)
    lng = Column(Float)


class University(Base, TimestampsMixin):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=False)
    created_by = Column(ForeignKey("users.id"))
    position_id = Column(ForeignKey("positions.id"))

    position = relationship("Position")
    buildings = relationship("Building")
    building_zones = relationship("BuildingZone", viewonly=True)


class BuildingZone(Base):
    __tablename__ = "building_zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    university_id = Column(ForeignKey("universities.id"))

    @property
    def university_slug(self) -> str:
        return self.university.slug    

    university = relationship("University")


class Building(Base, TimestampsMixin):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String, index=True)
    is_active = Column(Boolean, default=False)
    zone_id = Column(ForeignKey("building_zones.id"))
    created_by = Column(ForeignKey("users.id"))
    position_id = Column(ForeignKey("positions.id"))
    university_id = Column(ForeignKey("universities.id"))

    @property
    def zone(self):
        return self.building_zone.name

    building_zone = relationship("BuildingZone")
    creator = relationship("User")
    position = relationship("Position")
    rooms = relationship("Room")
    building_images = relationship("BuildingImage")


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
