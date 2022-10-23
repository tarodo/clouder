import datetime
import json

from app.api.packs import PacksErrors
from app.crud import packs
from app.models import User
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
    created_pack = r.json()
    pack = packs.read_by_id(db, created_pack["id"])
    assert created_pack
    assert pack
    assert created_pack["user_id"] == random_user.id
    assert created_pack["name"] == data["name"]
    assert created_pack["first_day"] == data["first_day"]
    assert created_pack["last_day"] == data["last_day"]
