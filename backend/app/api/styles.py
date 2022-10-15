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
