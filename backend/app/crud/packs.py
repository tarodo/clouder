from app.crud import common
from app.models import Pack, PackInDB, PackUpdate
from sqlmodel import Session, select


def read_one(
    db: Session, style_id: int | None, period_id: int | None
) -> list[Pack] | None:
    """Read one pack by style and period"""
    pass


def create(db: Session, payload: PackInDB) -> Pack:
    pass


def update(db: Session, db_obj: Pack, payload: PackUpdate) -> Pack:
    pass


def remove(db: Session, db_obj: Pack) -> Pack:
    pass
