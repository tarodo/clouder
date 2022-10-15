from app.models.users import User
from pydantic import constr
from sqlmodel import Field, Relationship, SQLModel


class StyleBase(SQLModel):
    name: constr(min_length=1) = Field(
        index=True, sa_column_kwargs={"unique": True}, nullable=False
    )
    base_link: constr(min_length=1) = Field(...)


class StyleBaseDB(StyleBase):
    user_id: int = Field(foreign_key="user.id")


class Style(StyleBaseDB, table=True):
    id: int = Field(primary_key=True)
    user: User = Relationship(back_populates="styles")


class StyleIn(StyleBaseDB):
    pass


class StyleOut(StyleBaseDB):
    id: int = Field(...)


class StyleUpdate(SQLModel):
    name: str | None = None
    base_link: str | None = None


class StyleInApi(StyleBase):
    pass
