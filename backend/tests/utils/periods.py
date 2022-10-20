import datetime
import random

from app.crud import periods
from app.models import Period, PeriodInDB, User
from sqlmodel import Session
from tests.utils.utils import random_lower_string


def create_random_period(db: Session, user: User) -> Period:
    """Create random period for the user"""
    period_in = PeriodInDB(
        user_id=user.id,
        name=random_lower_string(8),
        first_day=datetime.date.today(),
        last_day=datetime.date.today() + datetime.timedelta(days=7),
    )
    return periods.create(db, payload=period_in)


def create_random_periods(
    db: Session, user: User, cnt: int = None, min_cnt: int = 2, max_cnt: int = 10
) -> list[Period] | None:
    """Create list of periodЫ for the user"""
    if not cnt:
        if min_cnt and max_cnt:
            cnt = random.randint(min_cnt, max_cnt)
        else:
            return None
    return [create_random_period(db, user) for _ in range(cnt)]
