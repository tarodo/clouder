import datetime

from app.models.pack import Pack
from app.models.users import User
from sqlmodel import Field, Relationship, SQLModel


class BPSessionBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    pack_id: int = Field(foreign_key="pack.id")
    sheet_number: int = Field(..., ge=1)
    start_time: datetime.date = Field(...)
    is_finished: bool = Field(default=False)


class BPSessionBaseDB(BPSessionBase):
    pass


class BPSession(BPSessionBaseDB, table=True):
    id: int = Field(primary_key=True)

    pack: Pack = Relationship(back_populates="sessions")
    user: User = Relationship(back_populates="sessions")


class BPSessionInDB(BPSessionBaseDB):
    pass


class BPSessionOut(BPSessionBaseDB):
    id: int = Field(...)


class BPSessionInApi(BPSessionBase):
    pass
