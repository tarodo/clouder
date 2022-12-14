from app.crud import common
from app.models import Style, StyleInDB, StyleUpdate
from sqlmodel import Session, select


def read_by_name(db: Session, user_id: int, name: str) -> Style | None:
    """Read one style by name"""
    style = select(Style).where(Style.user_id == user_id).where(Style.name == name)
    style = db.exec(style).first()
    return style


def read_by_user_id(db: Session, user_id: int) -> list[Style] | None:
    """Read styles of the user"""
    user_styles = select(Style).where(Style.user_id == user_id)
    user_styles = db.exec(user_styles).all()
    return user_styles


def read_by_id(db: Session, style_id: int) -> Style | None:
    return common.read_by_id(db, Style, style_id)


def create(db: Session, payload: StyleInDB) -> Style:
    return common.create(db, Style, payload)


def update(db: Session, db_obj: Style, payload: StyleUpdate) -> Style:
    return common.update(db, db_obj, payload)


def remove(db: Session, db_obj: Style) -> Style:
    return common.remove(db, db_obj)
