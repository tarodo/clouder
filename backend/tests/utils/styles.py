import random

from app.crud import styles
from app.models import Style, StyleIn, User
from sqlmodel import Session
from tests.utils.utils import random_lower_string


def create_random_style(db: Session, user: User) -> Style:
    """Create random style for the user"""
    style_in = StyleIn(
        user_id=user.id, name=random_lower_string(8), base_link=random_lower_string(8)
    )
    return styles.create(db, payload=style_in)


def create_random_styles(
    db: Session, user: User, cnt: int = None, min_cnt: int = 2, max_cnt: int = 10
) -> list[Style] | None:
    """Create list of styles for the user"""
    if not cnt:
        if min_cnt and max_cnt:
            cnt = random.randint(2, 4)
        else:
            return None
    return [create_random_style(db, user) for _ in range(cnt)]
