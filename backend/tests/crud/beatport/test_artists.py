from app.crud.beatport import artists
from app.models import ArtistInDB
from sqlmodel import Session
from tests.utils.beatport import create_random_artist
from tests.utils.utils import random_bp_id, random_lower_string


def test_artist_create(db: Session) -> None:
    artist_in = ArtistInDB(
        name=random_lower_string(8),
        url=random_lower_string(8),
        bp_id=random_bp_id(),
    )
    artist = artists.create(db, payload=artist_in)
    assert artist.name == artist_in.name
    assert artist.url == artist_in.url
    assert artist.bp_id == artist_in.bp_id


def test_artist_read_by_id(db: Session) -> None:
    artist = create_random_artist(db)
    test_artist = artists.read_by_id(db, artist.id)
    assert test_artist == artist


def test_artist_read_by_name(db: Session) -> None:
    artist = create_random_artist(db)
    test_artist = artists.read_by_name(db, artist.name)
    assert test_artist == [artist]


def test_artist_read_by_bp_id(db: Session) -> None:
    artist = create_random_artist(db)
    test_artist = artists.read_by_bp_id(db, artist.bp_id)
    assert test_artist == artist


def test_artist_read_by_bp_id_wrong(db: Session) -> None:
    test_artist = artists.read_by_bp_id(db, -1)
    assert not test_artist


def test_artist_remove(db: Session) -> None:
    artist = create_random_artist(db)
    test_artist = artists.remove(db, artist)
    assert test_artist == artist
    remove_artist = artists.read_by_id(db, artist.id)
    assert not remove_artist
