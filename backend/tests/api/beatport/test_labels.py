import datetime
import json

from app.api.beatport.labels import LabelsErrors
from app.crud.beatport import labels
from app.models import User
from fastapi.testclient import TestClient
from sqlmodel import Session
from tests.utils.beatport import create_random_label
from tests.utils.users import (create_random_user,
                               get_authentication_token_from_email)
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
    r = client.get(f"/labels/", params=params, headers=user_token_headers)
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
    r = client.get(f"/labels/", params=params, headers=user_token_headers)
    assert 200 <= r.status_code < 300
    ret_labels = r.json()
    assert ret_labels
    assert len(ret_labels) == 1
    created_label = ret_labels[0]
    assert created_label["name"] == label.name
    assert created_label["url"] == label.url
    assert created_label["bp_id"] == label.bp_id
