from app.crud import styles
from app.models import User
from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.utils.styles import create_random_styles
from tests.utils.users import get_authentication_token_from_email
from tests.utils.utils import random_lower_string


def test_style_create(
    client: TestClient, db: Session, random_user: User
) -> None:
    data = {"name": random_lower_string(8), "base_link": random_lower_string(8)}
    user_token_headers = get_authentication_token_from_email(client=client, email=random_user.email, db=db)
    r = client.post(f"/styles/", headers=user_token_headers, json=data)
    assert 200 <= r.status_code < 300
    created_style = r.json()
    style = styles.read_by_id(db, created_style["id"])
    assert created_style
    assert style
    assert created_style["user_id"] == random_user.id
    assert style.user_id == random_user.id
    assert created_style["name"] == data["name"]
    assert style.name == data["name"]
    assert created_style["base_link"] == data["base_link"]
    assert style.base_link == data["base_link"]


def test_style_create_empty_name(
    client: TestClient, db: Session, random_user: User
) -> None:
    data = {"name": "", "base_link": random_lower_string(8)}
    user_token_headers = get_authentication_token_from_email(client=client, email=random_user.email, db=db)
    r = client.post(f"/styles/", headers=user_token_headers, json=data)
    assert r.status_code == 422


def test_style_create_empty_base_link(
    client: TestClient, db: Session, random_user: User
) -> None:
    data = {"name": random_lower_string(8), "base_link": ""}
    user_token_headers = get_authentication_token_from_email(client=client, email=random_user.email, db=db)
    r = client.post(f"/styles/", headers=user_token_headers, json=data)
    assert r.status_code == 422


def test_style_read_all_for_user(
    client: TestClient, db: Session, random_user: User
) -> None:
    styles_ids = set([one_style.id for one_style in create_random_styles(db, random_user)])
    user_token_headers = get_authentication_token_from_email(client=client, email=random_user.email, db=db)
    r = client.get(f"/styles/", headers=user_token_headers)
    assert 200 <= r.status_code < 300
    user_styles = r.json()
    assert set([one_style["id"] for one_style in user_styles]) == styles_ids
