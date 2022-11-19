from app.crud import common
from app.models import Artist, ArtistInDB
from sqlmodel import Session


def read_by_name(db: Session, name: str) -> list[Artist] | None:
    """Read artists by name"""
    artist = common.read_by_field_many(db, Artist.name, name)
    return artist


def read_by_bp_id(db: Session, bp_id: int) -> Artist | None:
    """Read artist by beatport id"""
    artist = common.read_by_field(db, Artist.bp_id, bp_id)
    return artist


def read_by_id(db: Session, artist_id: int) -> Artist | None:
    return common.read_by_id(db, Artist, artist_id)


def create(db: Session, payload: ArtistInDB) -> Artist:
    return common.create(db, Artist, payload)


def remove(db: Session, db_obj: Artist) -> Artist:
    return common.remove(db, db_obj)
