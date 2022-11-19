import datetime

from app.crud import periods
from app.models import PeriodInDB, PeriodUpdate, User
from sqlmodel import Session
from tests.utils.periods import create_random_period, create_random_periods
from tests.utils.utils import random_lower_string


def test_period_create(db: Session, random_user: User) -> None:
    period_in = PeriodInDB(
        user_id=random_user.id,
        name=random_lower_string(8),
        first_day=datetime.date.today(),
        last_day=datetime.date.today() + datetime.timedelta(days=7),
    )
    period = periods.create(db, payload=period_in)
    assert period.name == period_in.name
    assert period.first_day == period_in.first_day
    assert period.last_day == period_in.last_day
    assert period.user == random_user


def test_period_read_by_name(db: Session, random_user: User) -> None:
    period = create_random_period(db, random_user)
    test_period = periods.read_by_name(db, random_user.id, period.name)
    assert test_period == period


def test_period_read_by_user_id(db: Session, random_user: User) -> None:
    periods_ids = set(
        [one_period.id for one_period in create_random_periods(db, random_user)]
    )

    user_periods = periods.read_by_user_id(db, random_user.id)
    assert periods_ids == set([period.id for period in user_periods])


def test_period_read_by_id(db: Session, random_user: User) -> None:
    period = create_random_period(db, random_user)
    test_period = periods.read_by_id(db, period.id)
    assert test_period == period


def test_period_update_full(db, random_user) -> None:
    period = create_random_period(db, random_user)
    old_version = period.dict()
    period_update_in = PeriodUpdate(
        name=random_lower_string(8),
        first_day=period.first_day - datetime.timedelta(days=1),
        last_day=period.last_day + datetime.timedelta(days=1),
    )
    period_updated = periods.update(db, period, period_update_in)
    assert period_updated == period
    assert period_updated.name == period_update_in.name
    assert period_updated.first_day == period_update_in.first_day
    assert period_updated.last_day == period_update_in.last_day
    assert period_updated.name != old_version["name"]
    assert period_updated.first_day != old_version["first_day"]
    assert period_updated.last_day != old_version["last_day"]


def test_period_update_name(db, random_user) -> None:
    period = create_random_period(db, random_user)
    old_version = period.dict()
    period_update_in = PeriodUpdate(
        name=random_lower_string(8),
        first_day=period.first_day,
        last_day=period.last_day,
    )
    period_updated = periods.update(db, period, period_update_in)
    assert period_updated == period
    assert period_updated.name == period_update_in.name
    assert period_updated.name != old_version["name"]
    assert period_updated.first_day == old_version["first_day"]
    assert period_updated.last_day == old_version["last_day"]


def test_period_update_first_day(db, random_user) -> None:
    period = create_random_period(db, random_user)
    old_version = period.dict()
    period_update_in = PeriodUpdate(
        name=period.name,
        first_day=period.first_day - datetime.timedelta(days=1),
        last_day=period.last_day,
    )
    period_updated = periods.update(db, period, period_update_in)
    assert period_updated == period
    assert period_updated.first_day == period_update_in.first_day
    assert period_updated.name == old_version["name"]
    assert period_updated.first_day != old_version["first_day"]
    assert period_updated.last_day == old_version["last_day"]


def test_period_update_last_day(db, random_user) -> None:
    period = create_random_period(db, random_user)
    old_version = period.dict()
    period_update_in = PeriodUpdate(
        name=period.name,
        first_day=period.first_day,
        last_day=period.last_day + datetime.timedelta(days=1),
    )
    period_updated = periods.update(db, period, period_update_in)
    assert period_updated == period
    assert period_updated.last_day == period_update_in.last_day
    assert period_updated.name == old_version["name"]
    assert period_updated.first_day == old_version["first_day"]
    assert period_updated.last_day != old_version["last_day"]


def test_period_remove(db, random_user) -> None:
    period = create_random_period(db, random_user)
    period = periods.remove(db, period)
    test_period = periods.read_by_id(db, period.id)
    assert not test_period
