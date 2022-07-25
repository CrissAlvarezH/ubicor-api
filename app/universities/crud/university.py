from typing import List, Optional

from sqlalchemy.orm import Session

from app.auth.models import User

from app.universities.models import University, UniversityOwnership
from app.universities.crud.positions import create_position, update_position
from app.universities.schemas.universities import UniversityCreate


def get_university(db: Session, id: int) -> Optional[University]:
    return (
        db.query(University)
        .filter(University.is_active, University.id == id)
        .first()
    )


def get_university_by_slug(db: Session, slug: str) -> Optional[University]:
    return (
        db.query(University)
        .filter(University.is_active, University.slug == slug)
        .first()
    )


def list_universities_by_slugs(db: Session, slugs: List[str]) -> List[University]:
    return (
        db.query(University)
        .filter(University.slug.in_(slugs))
        .all()
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
        created_by=creator.id,
        is_active=True
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


def create_university_ownership(db: Session, university_id: int, user_id: int):
    ownership = UniversityOwnership(university_id=university_id, user_id=user_id)
    db.add(ownership)
    db.commit()


def is_owner(db: Session, university_id: int, user_id: int):
    result = (
        db.query(UniversityOwnership)
        .filter(
            UniversityOwnership.user_id == user_id,
            UniversityOwnership.university_id == university_id)
        .first()
    )
    return result is not None


def get_assigned_universities(db: Session, user_id: int) -> List[University]:
    return (
        db.query(University)
        .join(UniversityOwnership)
        .filter(University.id == UniversityOwnership.university_id)
        .filter(UniversityOwnership.user_id == user_id)
        .all()
    )


def delete_all_assigned_university(db: Session, user_id: int):
    db.query(UniversityOwnership) \
        .filter(UniversityOwnership.user_id == user_id) \
        .delete()
    db.commit()
