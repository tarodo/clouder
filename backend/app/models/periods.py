import datetime

from app.models.users import User
from pydantic import constr, root_validator
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

name_con = constr(min_length=1, max_length=127)


class PeriodBase(SQLModel):
    name: name_con = Field(index=True, sa_column_kwargs={"unique": True})
    first_day: datetime.date = Field(...)
    last_day: datetime.date = Field(...)

    @root_validator
    def last_not_early_first(cls, values):
        first_day, last_day = values.get("first_day"), values.get("last_day")
        if first_day and last_day:
            if first_day > last_day:
                raise ValueError(
                    "The last day should not be earlier than the first day"
                )
        return values


class PeriodBaseDB(PeriodBase):
    user_id: int = Field(foreign_key="user.id")


class Period(PeriodBaseDB, table=True):
    __table_args__ = (UniqueConstraint("user_id", "name"),)
    id: int = Field(primary_key=True)
    user: User = Relationship(back_populates="periods")

    packs: list["Pack"] | None = Relationship(back_populates="period")


class PeriodInDB(PeriodBaseDB):
    pass


class PeriodOut(PeriodBaseDB):
    id: int = Field(...)


class PeriodInApi(PeriodBase):
    pass


class PeriodUpdate(PeriodInApi):
    pass
