from app.models.users import User
from pydantic import constr
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

# TODO: Change vars to enums
name_con = constr(min_length=1)
link_con = constr(min_length=1)


class StyleBase(SQLModel):
    name: name_con = Field(index=True, nullable=False)
    base_link: link_con = Field(...)


class StyleBaseDB(StyleBase):
    user_id: int = Field(foreign_key="user.id")


class Style(StyleBaseDB, table=True):
    __table_args__ = (UniqueConstraint("user_id", "name"),)
    id: int = Field(primary_key=True)
    user: User = Relationship(back_populates="styles")


class StyleIn(StyleBaseDB):
    pass


class StyleOut(StyleBaseDB):
    id: int = Field(...)


class StyleUpdate(SQLModel):
    name: name_con | None = None
    base_link: link_con | None = None


class StyleInApi(StyleBase):
    pass
