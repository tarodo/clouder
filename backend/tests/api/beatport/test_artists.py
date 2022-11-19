from app.api.beatport.artists import ArtistsErrors
from app.crud.beatport import artists
from fastapi.testclient import TestClient
from sqlmodel import Session
from tests.utils.beatport import create_random_artist
from tests.utils.utils import random_bp_id


def test_artist_create(client: TestClient, db: Session, user_token_headers) -> None:
    data = {
        "name": "Exploited",
        "url": "https://www.beatport.com/artist/exploited/7600",
        "bp_id": random_bp_id(),
    }
    r = client.post(f"/artists/", headers=user_token_headers, json=data)
    assert 200 <= r.status_code < 300
    created_artist = r.json()
    assert created_artist
    assert created_artist["id"]
    artist = artists.read_by_id(db, created_artist["id"])
    assert artist
    assert created_artist["name"] == data["name"]
    assert created_artist["url"] == data["url"]
    assert created_artist["bp_id"] == data["bp_id"]
    assert created_artist["name"] == artist.name
    assert created_artist["url"] == artist.url
    assert created_artist["bp_id"] == artist.bp_id


def test_artist_get_by_name(
    client: TestClient, db: Session, user_token_headers
) -> None:
    artist = create_random_artist(db)
    create_random_artist(db, name=artist.name)
    params = {"name": artist.name}
    r = client.get(f"/artists/findByName", params=params, headers=user_token_headers)
    assert 200 <= r.status_code < 300
    ret_artists = r.json()
    assert ret_artists
    assert len(ret_artists) == 2
    assert all(art["name"] == artist.name for art in ret_artists)


def test_artist_get_by_bp_id(
    client: TestClient, db: Session, user_token_headers
) -> None:
    artist = create_random_artist(db)
    params = {"bp_id": artist.bp_id}
    r = client.get(f"/artists/findByBpId", params=params, headers=user_token_headers)
    assert 200 <= r.status_code < 300
    created_artist = r.json()
    assert created_artist
    assert created_artist["id"] == artist.id
    assert created_artist["name"] == artist.name
    assert created_artist["url"] == artist.url
    assert created_artist["bp_id"] == artist.bp_id


def test_artist_get_by_id(client: TestClient, db: Session, user_token_headers) -> None:
    artist = create_random_artist(db)
    create_random_artist(db, name=artist.name)
    r = client.get(f"/artists/{artist.id}", headers=user_token_headers)
    assert 200 <= r.status_code < 300
    created_artist = r.json()
    assert created_artist
    assert created_artist["id"] == artist.id
    assert created_artist["name"] == artist.name
    assert created_artist["url"] == artist.url
    assert created_artist["bp_id"] == artist.bp_id


def test_artist_get_by_wrong_id(
    client: TestClient, db: Session, user_token_headers
) -> None:
    artist = create_random_artist(db)
    create_random_artist(db, name=artist.name)
    wrong_id = artist.id + 100
    r = client.get(f"/artists/{wrong_id}", headers=user_token_headers)
    assert r.status_code == 400
    deleted_artist = r.json()
    assert deleted_artist["detail"]["type"] == str(ArtistsErrors.ArtistDoesNotExist)


def test_artist_remove_by_admin(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    artist = create_random_artist(db)
    create_random_artist(db, name=artist.name)
    r = client.delete(f"/artists/{artist.id}/", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    deleted_artist = r.json()
    assert deleted_artist
    assert deleted_artist["id"] == artist.id
    assert deleted_artist["name"] == artist.name
    assert deleted_artist["url"] == artist.url
    assert deleted_artist["bp_id"] == artist.bp_id
    test_artist = artists.read_by_id(db, artist.id)
    assert not test_artist


def test_artist_remove_by_user(
    client: TestClient, db: Session, user_token_headers
) -> None:
    artist = create_random_artist(db)
    create_random_artist(db, name=artist.name)
    r = client.delete(f"/artists/{artist.id}/", headers=user_token_headers)
    assert r.status_code == 400
    deleted_artist = r.json()
    assert deleted_artist["detail"]["type"] == str(ArtistsErrors.UserHasNoRights)


def test_artist_remove_wrong_id(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    artist = create_random_artist(db)
    create_random_artist(db, name=artist.name)
    wrong_id = artist.id + 100
    r = client.delete(f"/artists/{wrong_id}/", headers=superuser_token_headers)
    assert r.status_code == 400
    deleted_artist = r.json()
    assert deleted_artist["detail"]["type"] == str(ArtistsErrors.ArtistDoesNotExist)
