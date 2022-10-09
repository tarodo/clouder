from app.api.deps import DepsErrors
from app.api.users import UsersErrors
from app.core.config import settings
from app.crud import users
from app.models import UserIn
from fastapi.testclient import TestClient
from sqlmodel import Session
from tests.utils.users import get_user_authentication_headers
from tests.utils.utils import random_email, random_lower_string


def test_get_users_normal_user_me(
    client: TestClient, user_token_headers: dict[str, str]
) -> None:
    r = client.get(f"/users/me", headers=user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_admin"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


def test_unauth_user(client: TestClient) -> None:
    r = client.get(f"/users/me", headers={})
    assert r.status_code == 401


def test_wrong_token(client: TestClient) -> None:
    r = client.get(f"/users/me", headers={"Authorization": f"Bearer 1111"})
    current_user = r.json()
    assert r.status_code == 400
    assert current_user["detail"]["err"] == str(DepsErrors.NotValidCredentials)


def test_nonexistent_user(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserIn(email=email, password=password)
    user = users.create(db, payload=user_in)

    headers = get_user_authentication_headers(
        client=client, email=email, password=password
    )
    users.remove(db, user)

    r = client.get(f"/users/me", headers=headers)
    current_user = r.json()
    assert r.status_code == 400
    assert current_user["detail"]["err"] == str(DepsErrors.UserNotFound)


def test_create_user_new_email_admin(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    r = client.post(f"/users/", headers=superuser_token_headers, json=data)
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = users.read_by_email(db, email=email)
    assert user
    assert user.email == created_user["email"]


def test_create_user_new_email_not_admin(
    client: TestClient, user_token_headers: dict[str, str], db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    r = client.post(f"/users/", headers=user_token_headers, json=data)
    created_user = r.json()
    assert 400
    assert created_user["detail"]["err"] == str(UsersErrors.UserIsNotAdmin)


def test_create_user_existing_email(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserIn(email=email, password=password)
    users.create(db, payload=user_in)
    data = {"email": email, "password": password}
    r = client.post(f"/users/", headers=superuser_token_headers, json=data)
    created_user = r.json()
    assert r.status_code == 400
    assert created_user["detail"]["err"] == str(UsersErrors.UserWithEmailExists)
