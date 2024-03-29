from app.crud import common
from app.models import Artist, Label, Release, ReleaseInDB
from sqlmodel import Session


def read_by_name(db: Session, name: str) -> list[Release] | None:
    """Read releases by name"""
    release = common.read_by_field_many(db, Release.name, name)
    return release


def read_by_bp_id(db: Session, bp_id: int) -> Release | None:
    """Read release by beatport id"""
    release = common.read_by_field(db, Release.bp_id, bp_id)
    return release


def read_by_label_id(db: Session, label: Label) -> list[Release] | None:
    """Read releases by label id"""
    return label.releases


def read_by_artist(db: Session, artist: Artist) -> list[Release] | None:
    """Read releases by artist id"""
    return artist.releases


def read_by_id(db: Session, release_id: int) -> Release | None:
    return common.read_by_id(db, Release, release_id)


def add_artists(db: Session, release: Release, artists: list[Artist]) -> Release:
    for art in artists:
        release.artists.append(art)
    db.add(release)
    db.commit()
    db.refresh(release)
    return release


def create(db: Session, payload: ReleaseInDB, artists: list[Artist] | None) -> Release:
    one_release = common.create(db, Release, payload)
    if artists:
        one_release = add_artists(db, one_release, artists)
    return one_release


def remove(db: Session, db_obj: Release) -> Release:
    return common.remove(db, db_obj)


def make_audited(db: Session, release: Release) -> Release:
    release.audited = True
    db.add(release)
    db.commit()
    db.refresh(release)
    return release
