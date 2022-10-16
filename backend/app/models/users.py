from pydantic import EmailStr, constr
from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, sa_column_kwargs={"unique": True})
    is_admin: bool = Field(default=False)


class User(UserBase, table=True):
    id: int = Field(primary_key=True)
    password: str = Field(...)

    styles: "Style" = Relationship(back_populates="user")


class UserIn(UserBase):
    password: constr(min_length=6) = Field(...)


class UserOut(UserBase):
    id: int = Field(...)


class UserUpdate(SQLModel):
    email: EmailStr | None = None
    password: str | None = None
    is_admin: bool | None = None
