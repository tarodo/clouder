from app.crud import common
from app.models import Label, LabelInDB
from sqlmodel import Session


def read_by_name(db: Session, name: str) -> list[Label] | None:
    """Read labels by name"""
    label = common.read_by_field_many(db, Label.name, name)
    return label


def read_by_bp_id(db: Session, bp_id: int) -> Label | None:
    """Read label by beatport id"""
    label = common.read_by_field(db, Label.bp_id, bp_id)
    return label


def read_by_id(db: Session, label_id: int) -> Label | None:
    return common.read_by_id(db, Label, label_id)


def create(db: Session, payload: LabelInDB) -> Label:
    return common.create(db, Label, payload)


def remove(db: Session, db_obj: Label) -> Label:
    return common.remove(db, db_obj)
