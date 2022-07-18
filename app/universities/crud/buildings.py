from typing import Optional, Union, List

from sqlalchemy.orm import Session

from app.auth.models import User
from app.universities.crud.images import delete_image

from app.universities.crud.positions import create_position, update_position
from app.universities.crud.university import get_university_by_slug
from app.universities.models import Building, BuildingImage, BuildingZone, University
from app.universities.schemas.buildings import BuildingCreate


def create_building(
    db: Session, university_id: int, building_in: BuildingCreate, creator: User
) -> Building:
    position = create_position(db, building_in.position)
    zone = get_building_zone(db, building_in.zone, university_id=university_id)

    building = Building(
        name=building_in.name,
        code=building_in.code,
        created_by=creator.id,
        zone_id=zone.id,
        position_id=position.id,
        university_id=university_id,
        is_active=True
    )

    db.add(building)
    db.commit()
    db.refresh(building)

    return building


def get_building(db: Session, id: int) -> Optional[Building]:
    return (
        db.query(Building)
        .filter(Building.is_active, Building.id == id)
        .first()
    )


def update_building(
    db: Session, id: int, building_in: BuildingCreate
) -> Building:
    building = get_building(db, id)

    update_position(db, building.position.id, building_in.position)

    building.name = building_in.name
    building.code = building_in.code

    db.add(building)
    db.commit()
    db.refresh(building)

    return building


def delete_building(db: Session, id: int):
    building = get_building(db, id)
    building.is_active = False

    db.add(building)
    db.commit()


# Building zones

def create_building_zone(db: Session, university_slug: str, name: str) -> BuildingZone:
    university = get_university_by_slug(db, university_slug)
    if not university:
        raise ValueError(f"university '{university_slug}' doesn't exits")

    zone = BuildingZone(name=name, university_id=university.id)
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone


def list_building_zones(
    db: Session, university_slug: Optional[str] = None
) -> List[BuildingZone]:
    if university_slug:
        university = get_university_by_slug(db, university_slug)
        return university.building_zones if university else []

    return db.query(BuildingZone).all()


def get_building_zone(
    db: Session, name: str, university_id: Optional[int] = None,
    university_slug: Optional[str] = None
) -> Optional[BuildingZone]:
    query = db.query(BuildingZone, University) \
        .filter(BuildingZone.university_id == University.id) \
        .filter(BuildingZone.name == name)

    if university_id:
        query.filter(University.id == university_id)
    if university_slug:
        query.filter(University.slug == university_slug)

    result = query.first()
    if result:
        zone, _ = result
        return zone
    else:
        return None


def delete_building_zone(db: Session, building_zone_id: int):
    building_zone = db.query(BuildingZone).get(building_zone_id)
    db.delete(building_zone)
    db.commit()


# Building images

def attach_building_image(
    db: Session,
    building_id: int,
    image_id: int
) -> BuildingImage:
    building_image = BuildingImage(building_id=building_id, image_id=image_id)

    db.add(building_image)
    db.commit()
    db.refresh(building_image)

    return building_image


def delete_building_image(db: Session, image_id: int, building_id: int):
    building_image = (
        db.query(BuildingImage)
        .filter(
            BuildingImage.image_id == image_id,
            BuildingImage.building_id == building_id)
        .first()
    )
    if building_image:
        db.delete(building_image)
        db.commit()

    delete_image(db, image_id)
