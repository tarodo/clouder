from datetime import timedelta
from enum import Enum
from typing import Any

from app.api import deps
from app.api.tools import raise_400
from app.core import security
from app.core.config import settings
from app.crud import users
from app.models.token import Token
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session


class LoginErrors(Enum):
    IncorrectCredentials = "Incorrect email or password"
    UserIsNotBot = "User is not a bot"


router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = users.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise_400(LoginErrors.IncorrectCredentials)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = security.create_access_token(user.id, expires_delta=access_token_expires)
    return {
        "access_token": token,
        "token_type": "bearer",
    }
