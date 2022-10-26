from app.crud import common
from app.models import Label, LabelInDB
from sqlmodel import Session, select


def read_by_name(db: Session, name: str) -> list[Label] | None:
    """Read one label by name"""
    label = select(Label).where(Label.name == name)
    label = db.exec(label).first()
    return label


def read_by_id(db: Session, label_id: int) -> Label | None:
    return common.read_by_id(db, Label, label_id)


def create(db: Session, payload: LabelInDB) -> Label:
    return common.create(db, Label, payload)


def remove(db: Session, db_obj: Label) -> Label:
    return common.remove(db, db_obj)
