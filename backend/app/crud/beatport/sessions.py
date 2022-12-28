from app.crud import common
from app.models import Artist, Label, Release, ReleaseInDB
from sqlmodel import Session


# def read_by_user_id(db: Session, user_id: int) -> list[Session] | None:
#     """Read session by name"""
#     style = select(Style).where(Style.user_id == user_id).where(Style.name == name)
#     style = db.exec(style).first()
#     return style