from enum import Enum

from app.api import deps
from app.api.tools import raise_400
from app.crud import periods
from app.models import (Period, PeriodInApi, PeriodInDB, PeriodOut,
                        PeriodUpdate, User, responses)
from fastapi import APIRouter, Body, Depends
from sqlmodel import Session

router = APIRouter()


class PeriodsErrors(Enum):
    PeriodAlreadyExists = "Period already exists"
    UserHasNoAccess = "User has no access"
    PeriodDoesNotExist = "Period does not exist"


def check_to_read(user: User, one_period: Period) -> bool:
    """Check if the user has read permission"""
    if user.is_admin:
        return True
    if user is one_period.user:
        return True
    return False


def check_to_update(user: User, one_period: Period) -> bool:
    """Check if the user has update permission"""
    pass


def check_to_remove(user: User, one_period: Period) -> bool:
    """Check if the user has delete permission"""
    pass


create_examples = {}


@router.post("/", response_model=PeriodOut, status_code=200, responses=responses)
def create_period(
    payload: PeriodInApi = Body(examples=create_examples),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Period:
    """Create one period"""
    old_period = periods.read_by_name(db, current_user.id, payload.name)
    if old_period:
        raise_400(PeriodsErrors.PeriodAlreadyExists)
    period_in = PeriodInDB(**payload.dict(), user_id=current_user.id)
    period = periods.create(db, period_in)
    return period


@router.get("/", response_model=list[PeriodOut], status_code=200, responses=responses)
def read_my(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> list[Period] | None:
    """Retrieve all periods for the user"""
    user_periods = periods.read_by_user_id(db, current_user.id)
    return user_periods


@router.get(
    "/{period_id}/", response_model=PeriodOut, status_code=200, responses=responses
)
def read(
    period_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Period | None:
    """Retrieve a period by id"""
    one_period = periods.read_by_id(db, period_id)
    if one_period:
        if check_to_read(current_user, one_period):
            return one_period
    else:
        if current_user.is_admin:
            return raise_400(PeriodsErrors.PeriodDoesNotExist)
    return raise_400(PeriodsErrors.UserHasNoAccess)


@router.put(
    "/{period_id}/", response_model=PeriodOut, status_code=200, responses=responses
)
def update(
    period_id: int,
    payload: PeriodUpdate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Period | None:
    """Update the period for the user"""
    pass


@router.delete(
    "/{period_id}/", response_model=PeriodOut, status_code=200, responses=responses
)
def remove(
    period_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Period | None:
    """Remove the period by id"""
    pass
