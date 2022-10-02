from app.core.security import get_password_hash, verify_password
from app.models import User, UserIn, UserUpdate
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select


def read_by_email(db: Session, email: str) -> User | None:
    """Read one user by email"""
    user = select(User).where(User.email == email)
    user = db.exec(user).first()
    return user


def read_by_id(db: Session, user_id: int) -> User | None:
    """Read one user by id"""
    user = select(User).where(User.id == user_id)
    user = db.exec(user).one_or_none()
    return user


def create(db: Session, payload: UserIn) -> User:
    """Create a user"""
    user = User(**payload.dict())
    password_hashed = get_password_hash(payload.password)
    user.password = password_hashed
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, db_obj: User, payload: UserUpdate) -> User:
    """Update user's data"""
    obj_data = jsonable_encoder(db_obj)
    update_data = payload.dict(exclude_unset=True, exclude_none=True)
    for field in obj_data:
        if field in update_data:
            new_data = update_data[field]
            if field == "password":
                new_data = get_password_hash(update_data["password"])
            setattr(db_obj, field, new_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, db_obj: User) -> User:
    """Remove user from DB"""
    db.delete(db_obj)
    db.commit()
    return db_obj


def authenticate(db: Session, email: str, password: str) -> User | None:
    """Authenticate user by checking its password"""
    user = read_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
