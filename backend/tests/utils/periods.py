import datetime
import random

from app.crud import periods
from app.models import Period, PeriodInApi, PeriodInDB, User
from sqlmodel import Session
from tests.utils.utils import random_lower_string


def get_valid_period_dict() -> dict:
    """Return valid dict of period"""
    return {
        "name": random_lower_string(8),
        "first_day": str(datetime.date.today()),
        "last_day": str(datetime.date.today() + datetime.timedelta(days=7)),
    }


def get_valid_period_in() -> PeriodInApi:
    """Return valid PeriodInApi"""
    period_in = PeriodInApi(
        **get_valid_period_dict()
    )

    return period_in


def create_random_period(db: Session, user: User) -> Period:
    """Create random period for the user"""
    period_in = PeriodInDB(
        user_id=user.id,
        **get_valid_period_in().dict()
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



