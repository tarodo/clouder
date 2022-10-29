from app.api.beatport.labels import LabelsErrors
from app.crud.beatport import labels
from fastapi.testclient import TestClient
from sqlmodel import Session
from tests.utils.beatport import create_random_label
from tests.utils.utils import random_bp_id


def test_label_create(client: TestClient, db: Session, user_token_headers) -> None:
    data = {
        "name": "Exploited",
        "url": "https://www.beatport.com/label/exploited/7600",
        "bp_id": random_bp_id(),
    }
    r = client.post(f"/labels/", headers=user_token_headers, json=data)
    assert 200 <= r.status_code < 300
    created_label = r.json()
    assert created_label
    assert created_label["id"]
    label = labels.read_by_id(db, created_label["id"])
    assert label
    assert created_label["name"] == data["name"]
    assert created_label["url"] == data["url"]
    assert created_label["bp_id"] == data["bp_id"]
    assert created_label["name"] == label.name
    assert created_label["url"] == label.url
    assert created_label["bp_id"] == label.bp_id


def test_label_get_by_name(client: TestClient, db: Session, user_token_headers) -> None:
    label = create_random_label(db)
    create_random_label(db, name=label.name)
    params = {"name": label.name}
    r = client.get(f"/labels/findByName", params=params, headers=user_token_headers)
    assert 200 <= r.status_code < 300
    ret_labels = r.json()
    assert ret_labels
    assert len(ret_labels) == 2
    assert all(lab["name"] == label.name for lab in ret_labels)


def test_label_get_by_bp_id(
    client: TestClient, db: Session, user_token_headers
) -> None:
    label = create_random_label(db)
    params = {"bp_id": label.bp_id}
    r = client.get(f"/labels/findByBpId", params=params, headers=user_token_headers)
    assert 200 <= r.status_code < 300
    created_label = r.json()
    assert created_label
    assert created_label["id"] == label.id
    assert created_label["name"] == label.name
    assert created_label["url"] == label.url
    assert created_label["bp_id"] == label.bp_id


def test_label_get_by_id(client: TestClient, db: Session, user_token_headers) -> None:
    label = create_random_label(db)
    create_random_label(db, name=label.name)
    r = client.get(f"/labels/{label.id}", headers=user_token_headers)
    assert 200 <= r.status_code < 300
    created_label = r.json()
    assert created_label
    assert created_label["id"] == label.id
    assert created_label["name"] == label.name
    assert created_label["url"] == label.url
    assert created_label["bp_id"] == label.bp_id


def test_label_get_by_wrong_id(
    client: TestClient, db: Session, user_token_headers
) -> None:
    label = create_random_label(db)
    create_random_label(db, name=label.name)
    wrong_id = label.id + 100
    r = client.get(f"/labels/{wrong_id}", headers=user_token_headers)
    assert r.status_code == 400
    deleted_label = r.json()
    assert deleted_label["detail"]["type"] == str(LabelsErrors.LabelDoesNotExist)


def test_label_remove_by_admin(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    label = create_random_label(db)
    create_random_label(db, name=label.name)
    r = client.delete(f"/labels/{label.id}/", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    deleted_label = r.json()
    assert deleted_label
    assert deleted_label["id"] == label.id
    assert deleted_label["name"] == label.name
    assert deleted_label["url"] == label.url
    assert deleted_label["bp_id"] == label.bp_id
    test_label = labels.read_by_id(db, label.id)
    assert not test_label


def test_label_remove_by_user(
    client: TestClient, db: Session, user_token_headers
) -> None:
    label = create_random_label(db)
    create_random_label(db, name=label.name)
    r = client.delete(f"/labels/{label.id}/", headers=user_token_headers)
    assert r.status_code == 400
    deleted_label = r.json()
    assert deleted_label["detail"]["type"] == str(LabelsErrors.UserHasNoRights)


def test_label_remove_wrong_id(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    label = create_random_label(db)
    create_random_label(db, name=label.name)
    wrong_id = label.id + 100
    r = client.delete(f"/labels/{wrong_id}/", headers=superuser_token_headers)
    assert r.status_code == 400
    deleted_label = r.json()
    assert deleted_label["detail"]["type"] == str(LabelsErrors.LabelDoesNotExist)
