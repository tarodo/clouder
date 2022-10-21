import datetime
import json
import logging

from app.api.periods import PeriodsErrors
from app.crud import periods
from app.models import User
from fastapi.testclient import TestClient
from sqlmodel import Session
from tests.utils.periods import create_random_period, create_random_periods, get_valid_period_in, get_valid_period_dict
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


def test_period_create_first_eq_last(client: TestClient, db: Session, random_user: User) -> None:
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


def test_period_create_first_gt_last(client: TestClient, db: Session, random_user: User) -> None:
    data = get_valid_period_in().dict()
    data["first_day"] = data["last_day"] + datetime.timedelta(days=1)
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(f"/periods/", headers=user_token_headers, json=json.dumps(data, default=str))
    assert r.status_code == 422


def test_period_create_empty_name(client: TestClient, db: Session, random_user: User) -> None:
    data = get_valid_period_in().dict()
    data["name"] = ""
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(f"/periods/", headers=user_token_headers, json=json.dumps(data, default=str))
    assert r.status_code == 422


def test_period_create_none_name(client: TestClient, db: Session, random_user: User) -> None:
    data = get_valid_period_in().dict()
    del data["name"]
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(f"/periods/", headers=user_token_headers, json=json.dumps(data, default=str))
    assert r.status_code == 422


def test_period_create_empty_first_day(client: TestClient, db: Session, random_user: User) -> None:
    data = get_valid_period_in().dict()
    del data["first_day"]
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(f"/periods/", headers=user_token_headers, json=json.dumps(data, default=str))
    assert r.status_code == 422


def test_period_create_empty_last_day(client: TestClient, db: Session, random_user: User) -> None:
    data = get_valid_period_in().dict()
    del data["last_day"]
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(f"/periods/", headers=user_token_headers, json=json.dumps(data, default=str))
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
