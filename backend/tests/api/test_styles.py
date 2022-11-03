from app.api.styles import StylesErrors
from app.crud import styles
from app.models import User
from fastapi.testclient import TestClient
from sqlmodel import Session
from tests.utils.styles import create_random_style, create_random_styles
from tests.utils.users import (create_random_user,
                               get_authentication_token_from_email)
from tests.utils.utils import random_lower_string


def test_style_create(client: TestClient, db: Session, random_user: User) -> None:
    data = {"name": random_lower_string(8), "base_link": random_lower_string(8)}
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
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
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(f"/styles/", headers=user_token_headers, json=data)
    assert r.status_code == 422


def test_style_create_empty_base_link(
    client: TestClient, db: Session, random_user: User
) -> None:
    data = {"name": random_lower_string(8), "base_link": ""}
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.post(f"/styles/", headers=user_token_headers, json=data)
    assert r.status_code == 422


# TODO: Add tests of creating same styles different users
def test_style_create_same(client: TestClient, db: Session, random_user: User) -> None:
    data = {"name": random_lower_string(8), "base_link": random_lower_string(8)}
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    client.post(f"/styles/", headers=user_token_headers, json=data)
    r = client.post(f"/styles/", headers=user_token_headers, json=data)
    assert r.status_code == 400
    one_style = r.json()
    assert one_style["detail"]["type"] == str(StylesErrors.StyleAlreadyExists)


def test_style_read_all_for_user(
    client: TestClient, db: Session, random_user: User
) -> None:
    styles_ids = set(
        [one_style.id for one_style in create_random_styles(db, random_user)]
    )
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.get(f"/styles/", headers=user_token_headers)
    assert 200 <= r.status_code < 300
    user_styles = r.json()
    assert set([one_style["id"] for one_style in user_styles]) == styles_ids


def test_style_read_by_id(client: TestClient, db: Session, random_user: User) -> None:
    style = create_random_style(db, random_user)
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.get(f"/styles/{style.id}/", headers=user_token_headers)
    assert 200 <= r.status_code < 300
    user_style = r.json()
    style_db = styles.read_by_id(db, user_style["id"])
    assert style == style_db


def test_style_read_by_id_wrong_user(
    client: TestClient, db: Session, random_user: User
) -> None:
    another_user = create_random_user(db)
    style = create_random_style(db, another_user)
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.get(f"/styles/{style.id}/", headers=user_token_headers)
    assert r.status_code == 400
    one_style = r.json()
    assert one_style["detail"]["type"] == str(StylesErrors.UserHasNoAccess)


def test_style_read_by_id_admin(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    random_user = create_random_user(db)
    style = create_random_style(db, random_user)
    r = client.get(f"/styles/{style.id}/", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    user_style = r.json()
    style_db = styles.read_by_id(db, user_style["id"])
    assert style == style_db


def test_style_read_by_id_wrong_id(
    client: TestClient, db: Session, random_user: User
) -> None:
    style = create_random_style(db, random_user)
    wrong_id = style.id + 100
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.get(f"/styles/{wrong_id}/", headers=user_token_headers)
    assert r.status_code == 400
    one_style = r.json()
    assert one_style["detail"]["type"] == str(StylesErrors.UserHasNoAccess)


def test_style_read_by_id_wrong_id_admin(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    random_user = create_random_user(db)
    style = create_random_style(db, random_user)
    wrong_id = style.id + 100
    r = client.get(f"/styles/{wrong_id}/", headers=superuser_token_headers)
    assert r.status_code == 400
    one_style = r.json()
    assert one_style["detail"]["type"] == str(StylesErrors.StyleDoesNotExist)


def test_style_update(client: TestClient, db: Session, random_user: User) -> None:
    old_style = create_random_style(db, random_user)
    data = {"name": random_lower_string(8), "base_link": random_lower_string(8)}
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/styles/{old_style.id}/", headers=user_token_headers, json=data)
    assert 200 <= r.status_code < 300
    updated_style = r.json()
    assert updated_style["id"] == old_style.id
    assert updated_style["name"] == data["name"]
    assert updated_style["base_link"] == data["base_link"]


def test_style_update_admin_another(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    random_user = create_random_user(db)
    old_style = create_random_style(db, random_user)
    data = {"name": random_lower_string(8), "base_link": random_lower_string(8)}
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/styles/{old_style.id}/", headers=user_token_headers, json=data)
    assert 200 <= r.status_code < 300
    updated_style = r.json()
    assert updated_style["id"] == old_style.id
    assert updated_style["name"] == data["name"]
    assert updated_style["base_link"] == data["base_link"]


def test_style_update_empty_name(
    client: TestClient, db: Session, random_user: User
) -> None:
    old_style = create_random_style(db, random_user)
    data = {"name": "", "base_link": random_lower_string(8)}
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/styles/{old_style.id}/", headers=user_token_headers, json=data)
    assert r.status_code == 422


def test_style_update_empty_link(
    client: TestClient, db: Session, random_user: User
) -> None:
    old_style = create_random_style(db, random_user)
    data = {"name": random_lower_string(8), "base_link": ""}
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/styles/{old_style.id}/", headers=user_token_headers, json=data)
    assert r.status_code == 422


def test_style_update_none_name(
    client: TestClient, db: Session, random_user: User
) -> None:
    old_style = create_random_style(db, random_user)
    data = {"base_link": random_lower_string(8)}
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/styles/{old_style.id}/", headers=user_token_headers, json=data)
    assert r.status_code == 422


def test_style_update_none_link(
    client: TestClient, db: Session, random_user: User
) -> None:
    old_style = create_random_style(db, random_user)
    data = {"name": random_lower_string(8)}
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/styles/{old_style.id}/", headers=user_token_headers, json=data)
    assert r.status_code == 422


def test_style_update_wrong_id(
    client: TestClient, db: Session, random_user: User
) -> None:
    style = create_random_style(db, random_user)
    wrong_id = style.id + 100
    data = {"name": random_lower_string(8), "base_link": random_lower_string(8)}
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/styles/{wrong_id}/", headers=user_token_headers, json=data)
    assert r.status_code == 400
    one_style = r.json()
    assert one_style["detail"]["type"] == str(StylesErrors.UserHasNoAccess)


def test_style_update_wrong_id_admin(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    random_user = create_random_user(db)
    style = create_random_style(db, random_user)
    wrong_id = style.id + 100
    data = {"name": random_lower_string(8), "base_link": random_lower_string(8)}
    r = client.put(f"/styles/{wrong_id}/", headers=superuser_token_headers, json=data)
    assert r.status_code == 400
    one_style = r.json()
    assert one_style["detail"]["type"] == str(StylesErrors.StyleDoesNotExist)


def test_style_update_same_name(
    client: TestClient, db: Session, random_user: User
) -> None:
    style = create_random_style(db, random_user)
    style_same = create_random_style(db, random_user)
    data = {"name": style_same.name, "base_link": random_lower_string(8)}
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/styles/{style.id}/", headers=user_token_headers, json=data)
    assert r.status_code == 400
    one_style = r.json()
    assert one_style["detail"]["type"] == str(StylesErrors.StyleAlreadyExists)


def test_style_update_wrong_user(
    client: TestClient, db: Session, random_user: User
) -> None:
    another_user = create_random_user(db)
    style = create_random_style(db, another_user)
    data = {"name": random_lower_string(8), "base_link": random_lower_string(8)}
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.put(f"/styles/{style.id}/", headers=user_token_headers, json=data)
    assert r.status_code == 400
    one_style = r.json()
    assert one_style["detail"]["type"] == str(StylesErrors.UserHasNoAccess)


def test_style_remove(client: TestClient, db: Session, random_user: User) -> None:
    style = create_random_style(db, random_user)
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.delete(f"/styles/{style.id}/", headers=user_token_headers)
    assert 200 <= r.status_code < 300
    user_style = r.json()
    assert style.id == user_style["id"]
    style_db = styles.read_by_id(db, user_style["id"])
    assert not style_db


def test_style_remove_admin(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    random_user = create_random_user(db)
    style = create_random_style(db, random_user)
    r = client.delete(f"/styles/{style.id}/", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    user_style = r.json()
    assert style.id == user_style["id"]
    style_db = styles.read_by_id(db, user_style["id"])
    assert not style_db


def test_style_remove_wrong_id(
    client: TestClient, db: Session, random_user: User
) -> None:
    style = create_random_style(db, random_user)
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    wrong_id = style.id + 100
    r = client.delete(f"/styles/{wrong_id}/", headers=user_token_headers)
    assert r.status_code == 400
    one_style = r.json()
    assert one_style["detail"]["type"] == str(StylesErrors.UserHasNoAccess)


def test_style_remove_wrong_id_admin(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    random_user = create_random_user(db)
    style = create_random_style(db, random_user)
    wrong_id = style.id + 100
    r = client.delete(f"/styles/{wrong_id}/", headers=superuser_token_headers)
    assert r.status_code == 400
    one_style = r.json()
    assert one_style["detail"]["type"] == str(StylesErrors.StyleDoesNotExist)


def test_style_remove_wrong_user(
    client: TestClient, db: Session, random_user: User
) -> None:
    another_user = create_random_user(db)
    style = create_random_style(db, another_user)
    user_token_headers = get_authentication_token_from_email(
        client=client, email=random_user.email, db=db
    )
    r = client.delete(f"/styles/{style.id}/", headers=user_token_headers)
    assert r.status_code == 400
    one_style = r.json()
    assert one_style["detail"]["type"] == str(StylesErrors.UserHasNoRights)
