from pydantic import EmailStr, constr
from sqlmodel import Field, Relationship, SQLModel

pass_con = constr(min_length=6, max_length=255)


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, sa_column_kwargs={"unique": True})
    is_admin: bool = Field(default=False)


class User(UserBase, table=True):
    id: int = Field(primary_key=True)
    password: pass_con = Field(...)

    styles: list["Style"] = Relationship(back_populates="user")
    periods: list["Period"] = Relationship(back_populates="user")
    sessions: list["Session"] = Relationship(back_populates="user")


class UserIn(UserBase):
    password: pass_con = Field(...)


class UserOut(UserBase):
    id: int = Field(...)


class UserUpdate(SQLModel):
    email: EmailStr | None = None
    password: pass_con | None = None
    is_admin: bool | None = None
