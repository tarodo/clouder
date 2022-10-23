from app.crud import common
from app.models import Pack, PackInDB, PackUpdate
from sqlmodel import Session, select


def read_packs(
    db: Session, style_id: int | None = None, period_id: int | None = None
) -> list[Pack] | None:
    """Read one pack by style and period"""
    pack_query = select(Pack)
    if style_id:
        pack_query = pack_query.where(Pack.style_id == style_id)
    if period_id:
        pack_query = pack_query.where(Pack.period_id == period_id)
    pack = db.exec(pack_query).all()
    return pack


def read_by_id(db: Session, pack_id: int) -> Pack | None:
    return common.read_by_id(db, Pack, pack_id)


def create(db: Session, payload: PackInDB) -> Pack:
    return common.create(db, Pack, payload)


def update(db: Session, db_obj: Pack, payload: PackUpdate) -> Pack:
    return common.update(db, db_obj, payload)


def remove(db: Session, db_obj: Pack) -> Pack:
    return common.remove(db, db_obj)
