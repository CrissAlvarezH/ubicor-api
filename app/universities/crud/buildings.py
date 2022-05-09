from re import I
from typing import Optional

from sqlalchemy.orm import Session

from app.auth.models import User
from app.universities.crud.images import delete_image

from app.universities.crud.positions import create_position, update_position
from app.universities.models import Building, BuildingImage
from app.universities.schemas.buildings import BuildingCreate


def create_building(
    db: Session, university_id: int, building_in: BuildingCreate, creator: User
) -> Building:
    position = create_position(db, building_in.position)
    building = Building(
        name=building_in.name,
        code=building_in.code,
        created_by=creator.id,
        position_id=position.id,
        university_id=university_id
    )

    db.add(building)
    db.commit()
    db.refresh(building)

    return building


def get_building(db: Session, id: int) -> Optional[Building]:
    return (
        db.query(Building)
        .filter(Building
        .is_active, Building.id == id)
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
