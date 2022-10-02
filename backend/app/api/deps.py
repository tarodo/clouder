from enum import Enum
from typing import Generator

from app.api.tools import raise_400
from app.core.config import settings
from app.crud import users
from app.db import session
from app.models import User
from app.models.token import TokenPayload
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlmodel import Session


class DepsErrors(Enum):
    NotValidCredentials = "Could not validate credentials"
    UserNotFound = "User not found"


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token")


def get_db() -> Generator:
    try:
        db = session
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise_400(DepsErrors.NotValidCredentials)
    user = users.read_by_id(db, user_id=token_data.sub)
    if not user:
        raise_400(DepsErrors.UserNotFound)
    return user
