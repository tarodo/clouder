from app.models import Style, StyleIn, StyleUpdate
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select


def read_by_name(db: Session, name: str) -> Style | None:
    """Read one style by name"""
    style = select(Style).where(Style.name == name)
    style = db.exec(style).first()
    return style


def read_by_id(db: Session, style_id: int) -> Style | None:
    """Read one style by id"""
    style = select(Style).where(Style.id == style_id)
    style = db.exec(style).one_or_none()
    return style


def create(db: Session, payload: StyleIn) -> Style:
    """Create a style"""
    style = Style(**payload.dict())
    db.add(style)
    db.commit()
    db.refresh(style)
    return style


def update(db: Session, db_obj: Style, payload: StyleUpdate) -> Style:
    """Update style's data"""
    obj_data = jsonable_encoder(db_obj)
    update_data = payload.dict(exclude_unset=True, exclude_none=True)
    for field in obj_data:
        if field in update_data:
            new_data = update_data[field]
            setattr(db_obj, field, new_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, db_obj: Style) -> Style:
    """Remove style from DB"""
    db.delete(db_obj)
    db.commit()
    return db_obj
