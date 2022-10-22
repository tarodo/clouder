import datetime
import json
import logging

from app.api.periods import PeriodsErrors
from app.crud import periods
from app.models import User
from fastapi.testclient import TestClient
from sqlmodel import Session
from tests.utils.periods import (create_random_period, create_random_periods,
                                 get_valid_period_dict, get_valid_period_in)
from tests.utils.users import (create_random_user,
                               get_authentication_token_from_email)
from tests.utils.utils import random_lower_string


def test_period_create(client: TestClient, db: Session, random_user: User) -> None:
    data = get_valid_period_dict()
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(f"/periods/", headers=user_token_headers, json=data)
    created_period = r.json()
    period = periods.read_by_id(db, created_period["id"])
    assert created_period
    assert period
    assert created_period["user_id"] == random_user.id
    assert created_period["name"] == data["name"]
    assert created_period["first_day"] == data["first_day"]
    assert created_period["last_day"] == data["last_day"]


def test_period_create_first_eq_last(
    client: TestClient, db: Session, random_user: User
) -> None:
    data = get_valid_period_dict()
    data["last_day"] = data["first_day"]
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(f"/periods/", headers=user_token_headers, json=data)
    assert 200 <= r.status_code < 300
    created_period = r.json()
    period = periods.read_by_id(db, created_period["id"])
    assert created_period
    assert period
    assert created_period["user_id"] == random_user.id
    assert created_period["name"] == data["name"]
    assert created_period["first_day"] == data["first_day"]
    assert created_period["last_day"] == data["last_day"]


def test_period_create_first_gt_last(
    client: TestClient, db: Session, random_user: User
) -> None:
    data = get_valid_period_in().dict()
    data["first_day"] = data["last_day"] + datetime.timedelta(days=1)
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(
        f"/periods/", headers=user_token_headers, json=json.dumps(data, default=str)
    )
    assert r.status_code == 422


def test_period_create_empty_name(
    client: TestClient, db: Session, random_user: User
) -> None:
    data = get_valid_period_in().dict()
    data["name"] = ""
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(
        f"/periods/", headers=user_token_headers, json=json.dumps(data, default=str)
    )
    assert r.status_code == 422


def test_period_create_none_name(
    client: TestClient, db: Session, random_user: User
) -> None:
    data = get_valid_period_in().dict()
    del data["name"]
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(
        f"/periods/", headers=user_token_headers, json=json.dumps(data, default=str)
    )
    assert r.status_code == 422


def test_period_create_empty_first_day(
    client: TestClient, db: Session, random_user: User
) -> None:
    data = get_valid_period_in().dict()
    del data["first_day"]
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(
        f"/periods/", headers=user_token_headers, json=json.dumps(data, default=str)
    )
    assert r.status_code == 422


def test_period_create_empty_last_day(
    client: TestClient, db: Session, random_user: User
) -> None:
    data = get_valid_period_in().dict()
    del data["last_day"]
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(
        f"/periods/", headers=user_token_headers, json=json.dumps(data, default=str)
    )
    assert r.status_code == 422


def test_period_create_same(client: TestClient, db: Session, random_user: User) -> None:
    data = get_valid_period_dict()
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(f"/periods/", headers=user_token_headers, json=data)
    assert 200 <= r.status_code < 300
    r = client.post(f"/periods/", headers=user_token_headers, json=data)
    assert r.status_code == 400
    one_period = r.json()
    assert one_period["detail"]["type"] == str(PeriodsErrors.PeriodAlreadyExists)


def test_period_read_many_for_user(
    client: TestClient, db: Session, random_user: User
) -> None:
    periods_ids = set(
        [one_period.id for one_period in create_random_periods(db, random_user)]
    )
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.get(f"/periods/", headers=user_token_headers)
    assert 200 <= r.status_code < 300
    user_periods = r.json()
    assert set([one_period["id"] for one_period in user_periods]) == periods_ids


def test_period_read_by_id(client: TestClient, db: Session, random_user: User) -> None:
    period = create_random_period(db, random_user)
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.get(f"/periods/{period.id}/", headers=user_token_headers)
    assert 200 <= r.status_code < 300
    user_period = r.json()
    period_db = periods.read_by_id(db, user_period["id"])
    assert period == period_db


def test_period_read_by_id_wrong_user(
    client: TestClient, db: Session, random_user: User
) -> None:
    another_user = create_random_user(db)
    period = create_random_period(db, another_user)
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.get(f"/periods/{period.id}/", headers=user_token_headers)
    assert r.status_code == 400
    one_period = r.json()
    assert one_period["detail"]["type"] == str(PeriodsErrors.UserHasNoAccess)


def test_period_read_by_id_admin(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    random_user = create_random_user(db)
    period = create_random_period(db, random_user)
    r = client.get(f"/periods/{period.id}/", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    user_period = r.json()
    period_db = periods.read_by_id(db, user_period["id"])
    assert period == period_db


def test_period_read_by_id_wrong_id(
    client: TestClient, db: Session, random_user: User
) -> None:
    period = create_random_period(db, random_user)
    wrong_id = period.id + 100
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.get(f"/periods/{wrong_id}/", headers=user_token_headers)
    assert r.status_code == 400
    one_period = r.json()
    assert one_period["detail"]["type"] == str(PeriodsErrors.UserHasNoAccess)


def test_period_read_by_id_wrong_id_admin(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    random_user = create_random_user(db)
    period = create_random_period(db, random_user)
    wrong_id = period.id + 100
    r = client.get(f"/periods/{wrong_id}/", headers=superuser_token_headers)
    assert r.status_code == 400
    one_period = r.json()
    assert one_period["detail"]["type"] == str(PeriodsErrors.PeriodDoesNotExist)


def test_period_update(client: TestClient, db: Session, random_user: User) -> None:
    old_period = create_random_period(db, random_user)
    data = get_valid_period_dict()
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/periods/{old_period.id}/", headers=user_token_headers, json=data)
    assert 200 <= r.status_code < 300
    updated_period = r.json()
    assert updated_period["id"] == old_period.id
    assert updated_period["user_id"] == random_user.id
    assert updated_period["name"] == data["name"]
    assert updated_period["name"] != old_period.name
    assert updated_period["first_day"] == data["first_day"]
    assert updated_period["last_day"] == data["last_day"]


def test_period_update_admin(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    random_user = create_random_user(db)
    old_period = create_random_period(db, random_user)
    data = get_valid_period_dict()
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/periods/{old_period.id}/", headers=user_token_headers, json=data)
    assert 200 <= r.status_code < 300
    updated_period = r.json()
    assert updated_period["id"] == old_period.id
    assert updated_period["user_id"] == random_user.id
    assert updated_period["name"] == data["name"]
    assert updated_period["first_day"] == data["first_day"]
    assert updated_period["last_day"] == data["last_day"]


def test_period_update_empty_name(
    client: TestClient, db: Session, random_user: User
) -> None:
    old_period = create_random_period(db, random_user)
    data = get_valid_period_dict()
    data["name"] = ""
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/periods/{old_period.id}/", headers=user_token_headers, json=data)
    assert r.status_code == 422


def test_period_update_none_name(
    client: TestClient, db: Session, random_user: User
) -> None:
    old_period = create_random_period(db, random_user)
    data = get_valid_period_dict()
    del data["name"]
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/periods/{old_period.id}/", headers=user_token_headers, json=data)
    assert 200 <= r.status_code < 300
    updated_period = r.json()
    assert updated_period["id"] == old_period.id
    assert updated_period["user_id"] == random_user.id
    assert updated_period["name"] == old_period.name
    assert updated_period["first_day"] == data["first_day"]
    assert updated_period["last_day"] == data["last_day"]


def test_period_update_first_gt_last(
    client: TestClient, db: Session, random_user: User
) -> None:
    old_period = create_random_period(db, random_user)
    data = get_valid_period_dict()
    data["first_day"], data["last_day"] = data["last_day"], data["first_day"]
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/periods/{old_period.id}/", headers=user_token_headers, json=data)
    assert r.status_code == 422


def test_period_update_first_gt_last_first_only(
    client: TestClient, db: Session, random_user: User
) -> None:
    old_period = create_random_period(db, random_user)
    data = get_valid_period_dict()
    data["first_day"] = (old_period.last_day + datetime.timedelta(days=1)).strftime(
        "%Y-%m-%d"
    )
    del data["last_day"]
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/periods/{old_period.id}/", headers=user_token_headers, json=data)
    assert r.status_code == 400


def test_period_update_first_only(
    client: TestClient, db: Session, random_user: User
) -> None:
    old_period = create_random_period(db, random_user)
    data = get_valid_period_dict()
    data["first_day"] = (old_period.last_day - datetime.timedelta(days=1)).strftime(
        "%Y-%m-%d"
    )
    del data["last_day"]
    del data["name"]
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/periods/{old_period.id}/", headers=user_token_headers, json=data)
    assert 200 <= r.status_code < 300
    updated_period = r.json()
    assert updated_period["id"] == old_period.id
    assert updated_period["user_id"] == random_user.id
    assert updated_period["name"] == old_period.name
    assert updated_period["first_day"] == data["first_day"]
    assert updated_period["last_day"] == old_period.last_day.strftime("%Y-%m-%d")


def test_period_update_wrong_id(
    client: TestClient, db: Session, random_user: User
) -> None:
    period = create_random_period(db, random_user)
    wrong_id = period.id + 100
    data = get_valid_period_dict()
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/periods/{wrong_id}/", headers=user_token_headers, json=data)
    assert r.status_code == 400
    one_period = r.json()
    assert one_period["detail"]["type"] == str(PeriodsErrors.UserHasNoAccess)


def test_period_update_wrong_id_admin(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    random_user = create_random_user(db)
    period = create_random_period(db, random_user)
    wrong_id = period.id + 100
    data = get_valid_period_dict()
    r = client.put(f"/periods/{wrong_id}/", headers=superuser_token_headers, json=data)
    assert r.status_code == 400
    one_period = r.json()
    assert one_period["detail"]["type"] == str(PeriodsErrors.PeriodDoesNotExist)


def test_period_update_same_name(
    client: TestClient, db: Session, random_user: User
) -> None:
    period = create_random_period(db, random_user)
    period_same = create_random_period(db, random_user)
    data = get_valid_period_dict()
    data["name"] = period_same.name
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/periods/{period.id}/", headers=user_token_headers, json=data)
    assert r.status_code == 400
    one_period = r.json()
    assert one_period["detail"]["type"] == str(PeriodsErrors.PeriodAlreadyExists)


def test_period_update_wrong_user(
    client: TestClient, db: Session, random_user: User
) -> None:
    another_user = create_random_user(db)
    period = create_random_period(db, another_user)
    data = get_valid_period_dict()
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/periods/{period.id}/", headers=user_token_headers, json=data)
    assert r.status_code == 400
    one_period = r.json()
    assert one_period["detail"]["type"] == str(PeriodsErrors.UserHasNoAccess)
