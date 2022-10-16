import random

from app.crud import styles
from app.models import Style, StyleIn, StyleUpdate, User
from sqlmodel import Session
from tests.utils.styles import create_random_style, create_random_styles
from tests.utils.utils import random_lower_string


def test_style_create(db: Session, random_user: User) -> None:
    style_in = StyleIn(
        user_id=random_user.id,
        name=random_lower_string(8),
        base_link=random_lower_string(8),
    )
    style = styles.create(db, payload=style_in)
    assert style.name == style_in.name
    assert style.base_link == style_in.base_link
    assert style.user == random_user


def test_style_read_by_id(db: Session, random_user: User) -> None:
    style = create_random_style(db, random_user)
    test_style = styles.read_by_id(db, style.id)
    assert test_style == style


def test_style_read_by_name(db: Session, random_user: User) -> None:
    style = create_random_style(db, random_user)
    test_style = styles.read_by_name(db, random_user.id, style.name)
    assert test_style == style


def test_style_update_name(db, random_user) -> None:
    style = create_random_style(db, random_user)
    old_name = style.name
    style_update_in = StyleUpdate(name=random_lower_string(8))
    style_updated = styles.update(db, style, style_update_in)
    assert style_updated == style
    assert style_updated.name == style_update_in.name
    assert style_updated.name != old_name


def test_style_update_base_link(db, random_user) -> None:
    style = create_random_style(db, random_user)
    old_base_link = style.base_link
    style_update_in = StyleUpdate(base_link=random_lower_string(8))
    style_updated = styles.update(db, style, style_update_in)
    assert style_updated == style
    assert style_updated.base_link == style_update_in.base_link
    assert style_updated.base_link != old_base_link


def test_style_remove(db, random_user) -> None:
    style = create_random_style(db, random_user)
    style = styles.remove(db, style)
    test_style = styles.read_by_id(db, style.id)
    assert not test_style


def test_style_read_by_user_id(db: Session, random_user: User) -> None:
    styles_ids = set(
        [one_style.id for one_style in create_random_styles(db, random_user)]
    )

    user_styles = styles.read_by_user_id(db, random_user.id)
    assert styles_ids == set([style.id for style in user_styles])


def test_style_read_by_wrong_user_id(db: Session, random_user: User) -> None:
    user_styles = styles.read_by_user_id(db, 66666)
    assert not user_styles
