from app.crud.beatport import labels
from app.models import LabelInDB, User
from sqlmodel import Session
from tests.utils.beatport import create_random_label
from tests.utils.utils import random_bp_id, random_lower_string


def test_label_create(db: Session) -> None:
    label_in = LabelInDB(
        name=random_lower_string(8),
        url=random_lower_string(8),
        bp_id=random_bp_id(),
    )
    label = labels.create(db, payload=label_in)
    assert label.name == label_in.name
    assert label.url == label_in.url
    assert label.bp_id == label_in.bp_id


def test_label_read_by_id(db: Session) -> None:
    label = create_random_label(db)
    test_label = labels.read_by_id(db, label.id)
    assert test_label == label


def test_label_read_by_name(db: Session) -> None:
    label = create_random_label(db)
    test_label = labels.read_by_name(db, label.name)
    assert test_label == label
