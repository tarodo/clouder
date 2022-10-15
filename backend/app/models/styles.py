from app.models.users import User
from sqlmodel import Field, Relationship, SQLModel


class StyleBase(SQLModel):
    name: str = Field(index=True, sa_column_kwargs={"unique": True})
    base_link: str = Field(...)
    user_id: int = Field(foreign_key="user.id")


class Style(StyleBase, table=True):
    id: int = Field(primary_key=True)
    user: User = Relationship(back_populates="styles")


class StyleIn(StyleBase):
    pass


class StyleOut(StyleBase):
    id: int = Field(...)


class StyleUpdate(SQLModel):
    name: str | None = None
    base_link: str | None = None
