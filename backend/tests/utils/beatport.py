from app.crud.beatport import labels
from app.models import Label, LabelInDB
from sqlmodel import Session
from tests.utils.utils import random_bp_id, random_lower_string


def create_random_label(
    db: Session,
    name: str | None = None,
    url: str | None = None,
    bp_id: int | None = None,
) -> Label:
    """Create random label"""
    label_in = LabelInDB(
        name=name if name else random_lower_string(8),
        url=url if url else random_lower_string(8),
        bp_id=bp_id if bp_id else random_bp_id(),
    )
    return labels.create(db, payload=label_in)
