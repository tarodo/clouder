from app.models import Style, StyleIn, StyleUpdate
from sqlmodel import Session, select, SQLModel
from app.crud import common


def read_by_name(db: Session, name: str) -> Style | None:
    """Read one style by name"""
    style = select(Style).where(Style.name == name)
    style = db.exec(style).first()
    return style


def read_by_id(db: Session, style_id: int) -> SQLModel | None:
    return common.read_by_id(db, Style, style_id)


def create(db: Session, payload: StyleIn) -> SQLModel:
    return common.create(db, Style, payload)


def update(db: Session, db_obj: Style, payload: StyleUpdate) -> SQLModel:
    return common.update(db, db_obj, payload)


def remove(db: Session, db_obj: Style) -> SQLModel:
    return common.remove(db, db_obj)

