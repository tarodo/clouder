from app.crud.beatport import artists, labels, releases
from app.models import (Artist, ArtistInDB, Label, LabelInDB, Release,
                        ReleaseInDB)
from sqlmodel import Session
from tests.utils.utils import random_bp_id, random_lower_string


def create_random_label(
    db: Session,
    name: str | None = None,
    url: str | None = None,
    bp_id: int | None = None,
) -> Label:
    """Create random label"""
    label_in = LabelInDB(
        name=name if name else random_lower_string(8),
        url=url if url else random_lower_string(8),
        bp_id=bp_id if bp_id else random_bp_id(),
    )
    return labels.create(db, payload=label_in)


def create_random_artist(
    db: Session,
    name: str | None = None,
    url: str | None = None,
    bp_id: int | None = None,
) -> Artist:
    """Create random artist"""
    artist_in = ArtistInDB(
        name=name if name else random_lower_string(8),
        url=url if url else random_lower_string(8),
        bp_id=bp_id if bp_id else random_bp_id(),
    )
    return artists.create(db, payload=artist_in)


def create_random_release(
    db: Session,
    name: str | None = None,
    url: str | None = None,
    bp_id: int | None = None,
    label: Label | None = None,
    release_artists: list[Artist] | None = None,
) -> Release:
    """Create random release"""
    label = label if label else create_random_label(db)
    release_artists = (
        release_artists
        if release_artists
        else [create_random_artist(db) for _ in range(3)]
    )
    release_in = ReleaseInDB(
        name=name if name else random_lower_string(8),
        url=url if url else random_lower_string(8),
        bp_id=bp_id if bp_id else random_bp_id(),
        label_id=label.id,
    )
    return releases.create(db, payload=release_in, artists=release_artists)
