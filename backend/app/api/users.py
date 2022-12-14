from enum import Enum

from app.api import deps
from app.api.tools import raise_400
from app.crud import users
from app.models import User, UserIn, UserOut, responses
from fastapi import APIRouter, Body, Depends
from sqlmodel import Session

router = APIRouter()


class UsersErrors(Enum):
    UserIsNotAdmin = "User is not admin"
    UserWithEmailExists = "User with Email exists"


create_examples = {
    "work": {
        "summary": "A work example",
        "description": "A **work** item works correctly.",
        "value": {
            "email": "user@test.com",
            "password": "password",
        },
    },
    "short_pass": {
        "summary": "ERROR: short password",
        "description": "The password is too short",
        "value": {
            "email": "user_short@test.com",
            "password": "pass",
        },
    },
}


@router.post("/", response_model=UserOut, status_code=200, responses=responses)
def create_user(
    payload: UserIn = Body(examples=create_examples),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> User:
    """Create One User"""
    if not current_user.is_admin:
        raise_400(UsersErrors.UserIsNotAdmin)

    old_user = users.read_by_email(db, payload.email)
    if old_user:
        raise_400(UsersErrors.UserWithEmailExists)

    user = users.create(db, payload)
    return user


@router.get("/me", response_model=UserOut, status_code=200, responses=responses)
def get_me(
    current_user: User = Depends(deps.get_current_user),
) -> User:
    """Get current user."""
    return current_user
