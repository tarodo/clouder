from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, sa_column_kwargs={"unique": True})


class User(UserBase, table=True):
    id: int = Field(primary_key=True)
    password: str = Field(...)


class UserIn(UserBase):
    password: str = Field(...)


class UserOut(UserBase):
    id: int = Field(...)


class UserUpdate(SQLModel):
    email: EmailStr | None = None
    password: str | None = None
