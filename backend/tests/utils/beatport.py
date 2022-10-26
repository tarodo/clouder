from app.crud.beatport import labels
from app.models import Label, LabelInDB
from sqlmodel import Session
from tests.utils.utils import random_bp_id, random_lower_string


def create_random_label(db: Session) -> Label:
    """Create random label"""
    label_in = LabelInDB(
        name=random_lower_string(8),
        url=random_lower_string(8),
        bp_id=random_bp_id(),
    )
    return labels.create(db, payload=label_in)
