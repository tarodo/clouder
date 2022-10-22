from enum import Enum

from app.api import deps
from app.api.tools import raise_400
from app.crud import periods
from app.models import (Period, PeriodInApi, PeriodInDB, PeriodOut,
                        PeriodUpdate, User, responses)
from fastapi import APIRouter, Body, Depends
from pydantic import ValidationError
from sqlmodel import Session

router = APIRouter()


class PeriodsErrors(Enum):
    UserHasNoAccess = "User has no access"
    UserHasNoRights = "User has no rights"
    PeriodDoesNotExist = "Period does not exist"
    PeriodAlreadyExists = "Period already exists"
    FirstDayMustBeEarlier = "The last day should not be earlier than the first day"


def check_to_read(user: User, one_period: Period) -> bool:
    """Check if the user has read permission"""
    if user.is_admin:
        return True
    if user is one_period.user:
        return True
    return False


def check_to_update(user: User, one_period: Period) -> bool:
    """Check if the user has update permission"""
    return check_to_read(user, one_period)


def check_to_remove(user: User, one_period: Period) -> bool:
    """Check if the user has delete permission"""
    return check_to_read(user, one_period)


create_examples = {
    "work": {
        "summary": "A work example",
        "description": "A **work** item works correctly.",
        "value": {
            "name": "Week 48",
            "first_day": "2022-11-28",
            "last_day": "2022-12-04",
        },
    },
    "empty_name": {
        "summary": "ERROR: empty name",
        "value": {
            "name": "",
            "first_day": "2022-11-28",
            "last_day": "2022-12-04",
        },
    },
    "empty_first_day": {
        "summary": "ERROR: empty first_day",
        "value": {
            "name": "Week 33",
            "first_day": "",
            "last_day": "2022-12-04",
        },
    },
    "empty_last_day": {
        "summary": "ERROR: empty last_day",
        "value": {
            "name": "Week 13",
            "first_day": "2022-11-28",
            "last_day": "",
        },
    },
    "last_day_earlier": {
        "summary": "ERROR: last day earlier than first day",
        "value": {
            "name": "Week 13",
            "first_day": "2022-06-22",
            "last_day": "2022-04-10",
        },
    },
}

update_example = {
    "full_work": {
        "summary": "A work example for update",
        "value": {
            "name": "Week 1",
            "first_day": "2022-01-01",
            "last_day": "2022-01-02",
        },
    },
    "one_element_work": {
        "summary": "A work example for update one field",
        "value": {
            "name": "Week 100.2",
        },
    },
    "last_day_earlier": {
        "summary": "ERROR: last day earlier than first day",
        "value": {
            "name": "Week 33",
            "first_day": "2022-06-22",
            "last_day": "2022-01-01",
        },
    },
}


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
    payload: PeriodUpdate = Body(examples=update_example),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Period | None:
    """Update the period for the user"""
    one_period = periods.read_by_id(db, period_id)
    if not one_period:
        if current_user.is_admin:
            return raise_400(PeriodsErrors.PeriodDoesNotExist)
        return raise_400(PeriodsErrors.UserHasNoAccess)

    if not check_to_update(current_user, one_period):
        return raise_400(PeriodsErrors.UserHasNoAccess)

    if payload.name:
        if periods.read_by_name(db, current_user.id, payload.name):
            raise_400(PeriodsErrors.PeriodAlreadyExists)

    first_day, last_day = payload.first_day, payload.last_day
    if first_day or last_day:
        if not first_day:
            first_day = one_period.first_day
        if not last_day:
            last_day = one_period.last_day
        payload.first_day = first_day
        payload.last_day = last_day

    try:
        new_payload = PeriodUpdate(
            name=payload.name, first_day=first_day, last_day=last_day
        )
    except ValidationError as e:
        return raise_400(PeriodsErrors.FirstDayMustBeEarlier)

    return periods.update(db, one_period, new_payload)


@router.delete(
    "/{period_id}/", response_model=PeriodOut, status_code=200, responses=responses
)
def remove(
    period_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Period | None:
    """Remove the period by id"""
    one_period = periods.read_by_id(db, period_id)
    if not one_period:
        if current_user.is_admin:
            return raise_400(PeriodsErrors.PeriodDoesNotExist)
        return raise_400(PeriodsErrors.UserHasNoAccess)
    if not check_to_remove(current_user, one_period):
        return raise_400(PeriodsErrors.UserHasNoRights)

    return periods.remove(db, one_period)
