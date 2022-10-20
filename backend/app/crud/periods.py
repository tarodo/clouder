from app.crud import common
from app.models import Period, PeriodInDB, PeriodUpdate
from sqlmodel import Session, select


def read_by_name(db: Session, user_id: int, name: str) -> Period | None:
    """Read one period by name"""
    period = select(Period).where(Period.user_id == user_id).where(Period.name == name)
    period = db.exec(period).first()
    return period


def read_by_user_id(db: Session, user_id: int) -> list[Period] | None:
    """Read period of the user"""
    user_period = select(Period).where(Period.user_id == user_id)
    user_period = db.exec(user_period).all()
    return user_period


def read_by_id(db: Session, period_id: int) -> Period | None:
    return common.read_by_id(db, Period, period_id)


def create(db: Session, payload: PeriodInDB) -> Period:
    return common.create(db, Period, payload)


def update(db: Session, db_obj: Period, payload: PeriodUpdate) -> Period:
    return common.update(db, db_obj, payload)


def remove(db: Session, db_obj: Period) -> Period:
    return common.remove(db, db_obj)
