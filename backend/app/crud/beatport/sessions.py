from app.crud import common
from app.models import Artist, BPSession, Label, Release, ReleaseInDB, User
from sqlmodel import Session, select


def read_by_user_id(db: Session, user: User) -> list[BPSession] | None:
    """Read sessions by user_id"""
    return user.sessions


def read_last_by_user_id(db: Session, user: User) -> BPSession | None:
    """Read last session activation"""
    sessions = (
        select(BPSession)
        .where(BPSession.user == user.id)
        .order_by(BPSession.start_time)
    )
    sessions = db.exec(sessions).first()
    return sessions


def read_many_by_style_id(db: Session, style_id: int) -> list[BPSession] | None:
    """Read many sessions by style id"""
    pass


def read_last_by_style_id(db: Session, style_id: int) -> BPSession | None:
    """Read last session by style id"""
    pass


def read_many_by_pack_id(db: Session, style_id: int) -> list[BPSession] | None:
    """Read many sessions by pack id"""
    pass


def read_last_by_pack_id(db: Session, style_id: int) -> BPSession | None:
    """Read last session by pack id"""
    pass
