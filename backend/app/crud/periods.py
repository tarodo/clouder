from app.crud import common
from app.models import Period, PeriodInDB, PeriodUpdate
from sqlmodel import Session, select


def read_by_name(db: Session, user_id: int, name: str) -> Period | None:
    pass


def read_by_user_id(db: Session, user_id: int) -> list[Period] | None:
    pass


def read_by_id(db: Session, style_id: int) -> Period | None:
    pass


def create(db: Session, payload: PeriodInDB) -> Period:
    pass


def update(db: Session, db_obj: Period, payload: PeriodUpdate) -> Period:
    pass


def remove(db: Session, db_obj: Period) -> Period:
    pass
