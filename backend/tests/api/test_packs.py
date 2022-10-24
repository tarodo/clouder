import datetime
import json
import logging

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
    one_pack = r.json()
    assert one_pack["detail"]["type"] == str(PacksErrors.UserHasNoRights)


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
    one_pack = r.json()
    assert one_pack["detail"]["type"] == str(PacksErrors.UserHasNoRights)


def test_pack_create_same(client: TestClient, db: Session, random_user: User) -> None:
    data = get_valid_pack_dict(db, random_user)
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(f"/packs/", headers=user_token_headers, json=data)
    assert 200 <= r.status_code < 300
    r = client.post(f"/packs/", headers=user_token_headers, json=data)
    assert r.status_code == 400
    one_pack = r.json()
    assert one_pack["detail"]["type"] == str(PacksErrors.PackAlreadyExists)


def test_pack_read_by_style_period(
    client: TestClient, db: Session, random_user: User
) -> None:
    user_packs = create_random_packs(db, random_user)
    params = {"style_id": user_packs[0].style_id, "period_id": user_packs[0].period_id}
    pack_id = user_packs[0].id
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.get(f"/packs/", params=params, headers=user_token_headers)
    assert 200 <= r.status_code < 300
    ret_packs = r.json()
    one_pack = ret_packs[0]
    assert one_pack
    assert one_pack["id"] == pack_id


def test_pack_read_by_style(client: TestClient, db: Session, random_user: User) -> None:
    user_packs = create_random_packs(db, random_user)
    params = {
        "style_id": user_packs[0].style_id,
    }
    pack_ids = set(pack.id for pack in user_packs)
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.get(f"/packs/", params=params, headers=user_token_headers)
    assert 200 <= r.status_code < 300
    ret_packs = r.json()
    assert ret_packs
    ret_ids = set(one_pack["id"] for one_pack in ret_packs)
    assert ret_ids.issubset(pack_ids)


def test_pack_read_by_period(
    client: TestClient, db: Session, random_user: User
) -> None:
    user_packs = create_random_packs(db, random_user)
    params = {
        "period_id": user_packs[0].period_id,
    }
    pack_ids = set(pack.id for pack in user_packs)
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.get(f"/packs/", params=params, headers=user_token_headers)
    assert 200 <= r.status_code < 300
    ret_packs = r.json()
    assert ret_packs
    ret_ids = set(one_pack["id"] for one_pack in ret_packs)
    assert ret_ids.issubset(pack_ids)


def test_pack_read_another_style(
    client: TestClient, db: Session, random_user: User
) -> None:
    user_packs = create_random_packs(db, random_user, 3)
    another_user = create_random_user(db)
    another_pack = create_random_pack(db, another_user)
    params = {"style_id": another_pack.style_id, "period_id": user_packs[0].period_id}
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.get(f"/packs/", params=params, headers=user_token_headers)
    assert r.status_code == 400
    one_pack = r.json()
    assert one_pack["detail"]["type"] == str(PacksErrors.UserHasNoAccess)


def test_pack_read_another_period(
    client: TestClient, db: Session, random_user: User
) -> None:
    user_packs = create_random_packs(db, random_user, 3)
    another_user = create_random_user(db)
    another_pack = create_random_pack(db, another_user)
    params = {"style_id": user_packs[0].period_id, "period_id": another_pack.period_id}
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.get(f"/packs/", params=params, headers=user_token_headers)
    assert r.status_code == 400
    one_pack = r.json()
    assert one_pack["detail"]["type"] == str(PacksErrors.UserHasNoAccess)


def test_pack_read_empty(client: TestClient, db: Session, random_user: User) -> None:
    user_packs = create_random_packs(db, random_user)
    params = {}
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.get(f"/packs/", params=params, headers=user_token_headers)
    assert r.status_code == 400
    one_pack = r.json()
    assert one_pack["detail"]["type"] == str(PacksErrors.NotEnoughParams)


def test_pack_read_id(client: TestClient, db: Session, random_user: User) -> None:
    user_pack = create_random_pack(db, random_user)
    pack_id = user_pack.id
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.get(f"/packs/{pack_id}", headers=user_token_headers)
    assert 200 <= r.status_code < 300
    one_pack = r.json()
    assert one_pack
    assert one_pack["id"] == pack_id


def test_pack_read_id_by_admin(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    random_user = create_random_user(db)
    user_pack = create_random_pack(db, random_user)
    pack_id = user_pack.id
    r = client.get(f"/packs/{pack_id}", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    one_pack = r.json()
    assert one_pack
    assert one_pack["id"] == pack_id


def test_pack_read_id_another(
    client: TestClient, db: Session, random_user: User
) -> None:
    another_user = create_random_user(db)
    user_pack = create_random_pack(db, another_user)
    pack_id = user_pack.id
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.get(f"/packs/{pack_id}", headers=user_token_headers)
    assert r.status_code == 400
    one_pack = r.json()
    assert one_pack["detail"]["type"] == str(PacksErrors.UserHasNoAccess)


def test_pack_remove(client: TestClient, db: Session, random_user: User) -> None:
    user_pack = create_random_pack(db, random_user)
    pack_id = user_pack.id
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.delete(f"/packs/{pack_id}/", headers=user_token_headers)
    assert 200 <= r.status_code < 300
    one_pack = r.json()
    assert one_pack
    assert one_pack["id"] == pack_id
    pack_db = packs.read_by_id(db, pack_id)
    assert not pack_db


def test_pack_remove_by_admin(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    random_user = create_random_user(db)
    user_pack = create_random_pack(db, random_user)
    pack_id = user_pack.id
    r = client.delete(f"/packs/{pack_id}/", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    one_pack = r.json()
    assert one_pack
    assert one_pack["id"] == pack_id
    pack_db = packs.read_by_id(db, pack_id)
    assert not pack_db


def test_pack_remove_another(
    client: TestClient, db: Session, random_user: User
) -> None:
    another_user = create_random_user(db)
    user_pack = create_random_pack(db, another_user)
    pack_id = user_pack.id
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.delete(f"/packs/{pack_id}/", headers=user_token_headers)
    assert r.status_code == 400
    one_pack = r.json()
    assert one_pack["detail"]["type"] == str(PacksErrors.UserHasNoRights)
