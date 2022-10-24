import datetime
import json

from app.api.packs import PacksErrors
from app.crud import packs
from app.models import Pack, User
from fastapi.testclient import TestClient
from sqlmodel import Session
from tests.utils.packs import (create_random_pack, create_random_packs,
                               get_valid_pack_dict)
from tests.utils.users import (create_random_user,
                               get_authentication_token_from_email)


def test_pack_create(client: TestClient, db: Session, random_user: User) -> None:
    data = get_valid_pack_dict(db, random_user)
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(f"/packs/", headers=user_token_headers, json=data)
    assert 200 <= r.status_code < 300
    created_pack = r.json()
    assert created_pack
    assert created_pack["id"]
    pack = packs.read_by_id(db, created_pack["id"])
    assert pack
    assert created_pack["style_id"] == data["style_id"]
    assert created_pack["period_id"] == data["period_id"]
    assert created_pack["sheets_count"] == data["sheets_count"]
    assert created_pack["id"] == pack.id
    assert created_pack["style_id"] == pack.style_id
    assert created_pack["period_id"] == pack.period_id
    assert created_pack["sheets_count"] == pack.sheets_count


def test_pack_create_wrong_style(
    client: TestClient, db: Session, random_user: User
) -> None:
    data = get_valid_pack_dict(db, random_user)
    data["style_id"] = data["style_id"] + 100
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(f"/packs/", headers=user_token_headers, json=data)
    assert r.status_code == 400
    one_period = r.json()
    assert one_period["detail"]["type"] == str(PacksErrors.UserHasNoRights)


def test_pack_create_wrong_period(
    client: TestClient, db: Session, random_user: User
) -> None:
    data = get_valid_pack_dict(db, random_user)
    data["period_id"] = data["period_id"] + 100
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(f"/packs/", headers=user_token_headers, json=data)
    assert r.status_code == 400
    one_period = r.json()
    assert one_period["detail"]["type"] == str(PacksErrors.UserHasNoRights)


def test_pack_create_same(client: TestClient, db: Session, random_user: User) -> None:
    data = get_valid_pack_dict(db, random_user)
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(f"/packs/", headers=user_token_headers, json=data)
    assert 200 <= r.status_code < 300
    r = client.post(f"/packs/", headers=user_token_headers, json=data)
    assert r.status_code == 400
    one_period = r.json()
    assert one_period["detail"]["type"] == str(PacksErrors.PackAlreadyExists)
