from app.api.beatport.releases import ReleasesErrors
from app.crud.beatport import releases
from fastapi.testclient import TestClient
from sqlmodel import Session
from tests.utils.beatport import (create_random_artist, create_random_label,
                                  create_random_release)
from tests.utils.utils import random_bp_id


def test_release_create(client: TestClient, db: Session, user_token_headers) -> None:
    one_label = create_random_label(db)
    release_artists = [create_random_artist(db) for _ in range(3)]
    data = {
        "name": "Exploited",
        "url": "https://www.beatport.com/release/exploited/7600",
        "bp_id": random_bp_id(),
        "label_id": one_label.id,
        "artists_id": [art.id for art in release_artists],
    }
    r = client.post(f"/releases/", headers=user_token_headers, json=data)
    assert 200 <= r.status_code < 300
    created_release = r.json()
    assert created_release
    assert created_release["id"]
    assert created_release["name"] == data["name"]
    assert created_release["url"] == data["url"]
    assert created_release["bp_id"] == data["bp_id"]
    assert created_release["label"]
    assert created_release["label"]["id"] == data["label_id"]
    artists_id = set(art["id"] for art in created_release["artists"])
    assert artists_id == set(data["artists_id"])
    release = releases.read_by_id(db, created_release["id"])
    assert release
    assert release.name == data["name"]
    assert release.url == data["url"]
    assert release.bp_id == data["bp_id"]
    assert release.label_id == data["label_id"]
    artists_id = set(art.id for art in release.artists)
    assert artists_id == set(data["artists_id"])


def test_release_create_wrong_label(
    client: TestClient, db: Session, user_token_headers
) -> None:
    one_label = create_random_label(db)
    wrong_label_id = one_label.id + 100
    release_artists = [create_random_artist(db) for _ in range(3)]
    data = {
        "name": "Exploited",
        "url": "https://www.beatport.com/release/exploited/7600",
        "bp_id": random_bp_id(),
        "label_id": wrong_label_id,
        "artists_id": [art.id for art in release_artists],
    }
    r = client.post(f"/releases/", headers=user_token_headers, json=data)
    assert r.status_code == 400
    new_release = r.json()
    assert new_release["detail"]["type"] == str(ReleasesErrors.LabelDoesNotExists)
    assert new_release["detail"]["msg"] == str(
        ReleasesErrors.LabelDoesNotExists.value.format(wrong_label_id)
    )


def test_release_create_wrong_artist(
    client: TestClient, db: Session, user_token_headers
) -> None:
    one_label = create_random_label(db)
    one_artist = create_random_artist(db)
    wrong_artist_ids = [one_artist.id + 100, one_artist.id + 101]
    data = {
        "name": "Exploited",
        "url": "https://www.beatport.com/release/exploited/7600",
        "bp_id": random_bp_id(),
        "label_id": one_label.id,
        "artists_id": wrong_artist_ids,
    }
    r = client.post(f"/releases/", headers=user_token_headers, json=data)
    assert r.status_code == 400
    new_release = r.json()
    assert new_release["detail"]["type"] == str(ReleasesErrors.ArtistDoesNotExists)
    assert new_release["detail"]["msg"] == str(
        ReleasesErrors.ArtistDoesNotExists.value.format(wrong_artist_ids[0])
    )


def test_release_create_wrong_second_artist(
    client: TestClient, db: Session, user_token_headers
) -> None:
    one_label = create_random_label(db)
    one_artist = create_random_artist(db)
    wrong_artist_ids = [one_artist.id, one_artist.id + 101]
    data = {
        "name": "Exploited",
        "url": "https://www.beatport.com/release/exploited/7600",
        "bp_id": random_bp_id(),
        "label_id": one_label.id,
        "artists_id": wrong_artist_ids,
    }
    r = client.post(f"/releases/", headers=user_token_headers, json=data)
    assert r.status_code == 400
    new_release = r.json()
    assert new_release["detail"]["type"] == str(ReleasesErrors.ArtistDoesNotExists)
    assert new_release["detail"]["msg"] == str(
        ReleasesErrors.ArtistDoesNotExists.value.format(wrong_artist_ids[1])
    )


def test_release_read_by_label_id(
    client: TestClient, db: Session, user_token_headers
) -> None:
    one_label = create_random_label(db)
    releases_cnt = 3
    control_releases = [
        create_random_release(db, label=one_label) for _ in range(releases_cnt)
    ]
    control_ids = [control_release.id for control_release in control_releases]
    params = {"label_id": one_label.id}
    r = client.get(
        f"/releases/findByLabelId", params=params, headers=user_token_headers
    )
    assert 200 <= r.status_code < 300
    read_releases = r.json()
    assert len(read_releases) == releases_cnt
    assert all([one_release["id"] in control_ids for one_release in read_releases])


def test_release_read_by_artist_id(
    client: TestClient, db: Session, user_token_headers
) -> None:
    one_artist = create_random_artist(db)
    releases_cnt = 3
    control_releases = [
        create_random_release(db, release_artists=[one_artist])
        for _ in range(releases_cnt)
    ]
    control_ids = [control_release.id for control_release in control_releases]
    params = {"artist_id": one_artist.id}
    r = client.get(
        f"/releases/findByArtistId", params=params, headers=user_token_headers
    )
    assert 200 <= r.status_code < 300
    read_releases = r.json()
    assert len(read_releases) == releases_cnt
    assert all([one_release["id"] in control_ids for one_release in read_releases])
