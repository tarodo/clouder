from app.crud import users
from app.models import User, UserIn
from sqlmodel import Session
from tests.utils.utils import random_email, random_lower_string


def create_random_user(db: Session) -> User:
    """Return new user with random email and pass"""
    email = random_email()
    password = random_lower_string()
    user_in = UserIn(email=email, password=password)
    user = users.create(db, user_in)
    return user
