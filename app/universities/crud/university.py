from typing import List, Optional

from sqlalchemy.orm import Session

from app.auth.models import User

from app.universities.models import University
from app.universities.crud.positions import create_position, update_position
from app.universities.schemas.universities import UniversityCreate


def get_university(db: Session, id: int) -> Optional[University]:
    return (
        db.query(University)
        .filter(University.is_active, University.id == id)
        .first()
    )


def list_universities(
    db: Session, page: int = 1, page_size: int = 25
) -> List[University]:
    return (
        db.query(University)
        .filter(University.is_active)
        .limit(page_size)
        .offset(page - 1)
        .all()
    )


def create_university(
    db: Session, university_in: UniversityCreate, creator: User
) -> University:
    position = create_position(db, university_in.position)

    university = University(
        name=university_in.name, 
        slug=university_in.slug,
        position_id=position.id, 
        created_by=creator.id
    )

    db.add(university)
    db.commit()
    db.refresh(university)

    return university


def update_university(
    db: Session, id: int, university_in: UniversityCreate
) -> University:
    university = get_university(db, id)

    update_position(db, university.position_id, university_in.position)

    university.name = university_in.name
    university.slug = university_in.slug

    db.add(university)
    db.commit()
    db.refresh(university)

    return university


def delete_university(db: Session, id: int):
    university = get_university(db, id)
    university.is_active = False
    db.add(university)
    db.commit()
