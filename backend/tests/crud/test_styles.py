import pytest
from app.crud import styles
from app.models import StyleIn
from fastapi.encoders import jsonable_encoder
from pydantic.error_wrappers import ValidationError
from sqlmodel import Session
from tests.utils.users import create_random_user
from tests.utils.utils import random_lower_string


def test_style_create(db: Session) -> None:
    style_in = StyleIn(name=random_lower_string(8), base_link=random_lower_string(8))
    student = styles.create(db, payload=style_in)
    assert student.name == style_in.name
    assert student.base_link == style_in.base_link
