from app.crud.beatport import releases
from app.models import ReleaseInDB
from sqlmodel import Session
from tests.utils.beatport import (create_random_artist, create_random_label,
                                  create_random_release)
from tests.utils.utils import random_bp_id, random_lower_string


def test_release_create(db: Session) -> None:
    label = create_random_label(db)
    artists = [create_random_artist(db) for _ in range(3)]
    ReleaseInDB.update_forward_refs()
    release_in = ReleaseInDB(
        name=random_lower_string(8),
        url=random_lower_string(8),
        bp_id=random_bp_id(),
        label_id=label.id,
    )
    release = releases.create(db, payload=release_in, artists=artists)
    assert release.name == release_in.name
    assert release.url == release_in.url
    assert release.bp_id == release_in.bp_id
    assert release.label_id == release_in.label_id
    assert len(release.artists) == 3


def test_release_create_wo_artists(db: Session) -> None:
    label = create_random_label(db)
    ReleaseInDB.update_forward_refs()
    release_in = ReleaseInDB(
        name=random_lower_string(8),
        url=random_lower_string(8),
        bp_id=random_bp_id(),
        label_id=label.id,
    )
    release = releases.create(db, payload=release_in, artists=None)
    assert release.name == release_in.name
    assert release.url == release_in.url
    assert release.bp_id == release_in.bp_id
    assert release.label_id == release_in.label_id
    assert len(release.artists) == 0


def test_release_create_wo_label(db: Session) -> None:
    ReleaseInDB.update_forward_refs()
    release_in = ReleaseInDB(
        name=random_lower_string(8),
        url=random_lower_string(8),
        bp_id=random_bp_id(),
        label_id=None,
    )
    release = releases.create(db, payload=release_in, artists=None)
    assert release.name == release_in.name
    assert release.url == release_in.url
    assert release.bp_id == release_in.bp_id
    assert release.label_id is None
    assert len(release.artists) == 0


def test_release_read_by_id(db: Session) -> None:
    release = create_random_release(db)
    test_release = releases.read_by_id(db, release.id)
    assert release.id == test_release.id
    assert release.name == test_release.name
    assert release.url == test_release.url
    assert release.bp_id == test_release.bp_id
    assert release.label_id == test_release.label_id
    assert release.artists == test_release.artists


def test_release_read_by_bp_name(db: Session) -> None:
    release = create_random_release(db)
    test_release = releases.read_by_name(db, release.name)[0]
    assert release.id == test_release.id
    assert release.name == test_release.name
    assert release.url == test_release.url
    assert release.bp_id == test_release.bp_id
    assert release.label_id == test_release.label_id
    assert release.artists == test_release.artists


def test_release_read_by_bp_id(db: Session) -> None:
    release = create_random_release(db)
    test_release = releases.read_by_bp_id(db, release.bp_id)
    assert release.id == test_release.id
    assert release.name == test_release.name
    assert release.url == test_release.url
    assert release.bp_id == test_release.bp_id
    assert release.label_id == test_release.label_id
    assert release.artists == test_release.artists


def test_release_remove(db: Session) -> None:
    release = create_random_release(db)
    release_id = release.id
    test_release = releases.remove(db, release)
    remove_release = releases.read_by_id(db, release_id)
    assert not remove_release
