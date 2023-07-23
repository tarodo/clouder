from app.crud import common
from app.models import Pack, PackInDB, PackRelease, PackReleaseInDB, Release
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


def remove(db: Session, db_obj: Pack) -> Pack:
    return common.remove(db, db_obj)


def add_release(db: Session, pack: Pack, release: Release) -> Pack:
    new_pack_release = PackRelease(pack=pack, release=release)
    db.add(new_pack_release)
    db.commit()
    db.refresh(pack)
    return pack


def read_pack_release(db: Session, pack: Pack, release: Release) -> PackRelease:
    pack_release_query = select(PackRelease)
    pack_release_query = pack_release_query.where(PackRelease.pack == pack).where(
        PackRelease.release == release
    )
    pack_release = db.exec(pack_release_query).one()
    return pack_release
