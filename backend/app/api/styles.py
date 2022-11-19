from enum import Enum

from app.api import deps
from app.api.tools import raise_400
from app.crud import styles
from app.models import (Style, StyleInApi, StyleInDB, StyleOut, StyleUpdate,
                        User, responses)
from fastapi import APIRouter, Body, Depends, Path
from sqlmodel import Session

router = APIRouter()


class StylesErrors(Enum):
    UserHasNoAccess = "User has no access"
    UserHasNoRights = "User has no rights"
    StyleDoesNotExist = "Style does not exist"
    StyleAlreadyExists = "Style already exists"


def check_to_read(user: User, one_style: Style) -> bool:
    """Check if the user has read permission"""
    if user.is_admin:
        return True
    if user is one_style.user:
        return True
    return False


def check_to_update(user: User, one_style: Style) -> bool:
    """Check if the user has update permission"""
    return check_to_read(user, one_style)


def check_to_remove(user: User, one_style: Style) -> bool:
    """Check if the user has delete permission"""
    return check_to_read(user, one_style)


create_examples = {
    "work": {
        "summary": "A work example",
        "description": "A **work** item works correctly.",
        "value": {
            "name": "New style",
            "base_link": "bp/style/10332",
        },
    },
    "empty_name": {
        "summary": "ERROR: empty name",
        "value": {
            "name": "",
            "base_link": "bp/empty_name/10332",
        },
    },
    "empty_base_link": {
        "summary": "ERROR: empty base link",
        "value": {
            "name": "base_link",
            "base_link": "",
        },
    },
}


@router.post("/", response_model=StyleOut, status_code=200, responses=responses)
def create_style(
    payload: StyleInApi = Body(examples=create_examples),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Style:
    """Create one style"""
    old_style = styles.read_by_name(db, current_user.id, payload.name)
    if old_style:
        raise_400(StylesErrors.StyleAlreadyExists)
    style_in = StyleInDB(**payload.dict(), user_id=current_user.id)
    style = styles.create(db, style_in)
    return style


@router.get("/", response_model=list[StyleOut], status_code=200, responses=responses)
def read_my(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> list[Style] | None:
    """Retrieve all styles for the user"""
    user_styles = styles.read_by_user_id(db, current_user.id)
    return user_styles


@router.get(
    "/{style_id}/", response_model=StyleOut, status_code=200, responses=responses
)
def read(
    style_id: int = Path(..., gt=0),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Style | None:
    """Retrieve a style by id"""
    one_style = styles.read_by_id(db, style_id)
    if one_style:
        if check_to_read(current_user, one_style):
            return one_style
    else:
        if current_user.is_admin:
            return raise_400(StylesErrors.StyleDoesNotExist)
    return raise_400(StylesErrors.UserHasNoAccess)


@router.put(
    "/{style_id}/", response_model=StyleOut, status_code=200, responses=responses
)
def update(
    style_id: int = Path(..., gt=0),
    payload: StyleUpdate = Body(...),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Style | None:
    """Update the style for the user"""
    one_style = styles.read_by_id(db, style_id)
    if not one_style:
        if current_user.is_admin:
            return raise_400(StylesErrors.StyleDoesNotExist)
        return raise_400(StylesErrors.UserHasNoAccess)
    if payload.name:
        if styles.read_by_name(db, current_user.id, payload.name):
            raise_400(StylesErrors.StyleAlreadyExists)
    if not check_to_update(current_user, one_style):
        return raise_400(StylesErrors.UserHasNoAccess)

    return styles.update(db, one_style, payload)


@router.delete(
    "/{style_id}/", response_model=StyleOut, status_code=200, responses=responses
)
def remove(
    style_id: int = Path(..., gt=0),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Style | None:
    """Remove the style by id"""
    one_style = styles.read_by_id(db, style_id)
    if not one_style:
        if current_user.is_admin:
            return raise_400(StylesErrors.StyleDoesNotExist)
        return raise_400(StylesErrors.UserHasNoAccess)
    if not check_to_remove(current_user, one_style):
        return raise_400(StylesErrors.UserHasNoRights)

    return styles.remove(db, one_style)
