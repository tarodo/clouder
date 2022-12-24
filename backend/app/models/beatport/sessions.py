import datetime

from app.models import Pack, User
from sqlmodel import Field, Relationship, SQLModel


class SessionBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    pack_id: int = Field(foreign_key="pack.id")
    sheet_number: int = Field(..., ge=1)
    start_time: datetime.date = Field(...)
    is_finished: bool = Field(default=False)


class SessionBaseDB(SessionBase):
    pass


class Session(SessionBaseDB, table=True):
    id: int = Field(primary_key=True)

    pack: Pack = Relationship(back_populates="sessions")
    user: User = Relationship(back_populates="sessions")


class SessionInDB(SessionBaseDB):
    pass


class SessionOut(SessionBaseDB):
    id: int = Field(...)


class SessionInApi(SessionBase):
    pass
