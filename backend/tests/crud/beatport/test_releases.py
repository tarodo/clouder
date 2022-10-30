from app.crud.beatport import releases
from app.models import ReleaseInDB
from sqlmodel import Session
from tests.utils.beatport import create_random_artist, create_random_label
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
