from enum import Enum

from app.api import deps
from app.crud import styles
from app.models import Style, StyleIn, StyleInApi, StyleOut, User, responses
from fastapi import APIRouter, Depends
from sqlmodel import Session

router = APIRouter()


class StylesErrors(Enum):
    pass


@router.post("/", response_model=StyleOut, status_code=200, responses=responses)
def create_style(
    payload: StyleInApi,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Style:
    """Create one style"""
    style_in = StyleIn(**payload.dict(), user_id=current_user.id)
    style = styles.create(db, style_in)
    return style


@router.get("/", response_model=list[StyleOut], status_code=200, responses=responses)
def read_my(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> list[Style] | None:
    """Read all styles for the user"""
    user_styles = styles.read_by_user_id(db, current_user.id)
    return user_styles
