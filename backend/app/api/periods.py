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


def check_to_read(user: User, one_period: Period) -> bool:
    """Check if the user has read permission"""
    pass


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
    pass


@router.get("/", response_model=list[PeriodOut], status_code=200, responses=responses)
def read_my(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> list[Period] | None:
    """Retrieve all periods for the user"""
    pass


@router.get(
    "/{period_id}/", response_model=PeriodOut, status_code=200, responses=responses
)
def read(
    period_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Period | None:
    """Retrieve a period for the user"""
    pass


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
