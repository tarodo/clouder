import datetime

from app.models.users import User
from pydantic import EmailStr, constr
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

name_con = constr(min_length=1)


class PeriodBase(SQLModel):
    name: name_con = Field(index=True, sa_column_kwargs={"unique": True})
    first_day: datetime.date = Field(...)
    last_day: datetime.date = Field(...)


class PeriodBaseDB(PeriodBase):
    user_id: int = Field(foreign_key="user.id")


class Period(PeriodBaseDB, table=True):
    __table_args__ = (UniqueConstraint("user_id", "name"),)
    id: int = Field(primary_key=True)
    user: User = Relationship(back_populates="periods")


class PeriodInDB(PeriodBaseDB):
    pass


class PeriodOut(PeriodBaseDB):
    id: int = Field(...)


class PeriodUpdate(SQLModel):
    name: name_con | None = None
    first_day: datetime.date | None = None
    last_day: datetime.date | None = None


class PeriodInApi(PeriodBase):
    pass
