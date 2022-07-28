from typing import Optional

from sqlalchemy.orm import Session

from app.universities.models import Image


def create_image(
    db: Session,
    small: Optional[str] = None,
    medium: Optional[str] = None,
    original: Optional[str] = None,
) -> Image:
    image = Image(small=small, medium=medium, original=original)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def get_image(db: Session, id: int) -> Optional[Image]:
    return db.query(Image).filter(Image.id == id).first()


def update_image(
    db: Session,
    id: int,
    small: Optional[str] = None,
    medium: Optional[str] = None,
    original: Optional[str] = None,
) -> Image:
    image = get_image(db, id)

    if small:
        image.small = small
    if medium:
        image.medium = medium
    if original:
        image.original = original

    db.add(image)
    db.commit()
    db.refresh(image)

    return image


def delete_image(db: Session, id: int):
    image = get_image(db, id)
    db.delete(image)
    db.commit()
