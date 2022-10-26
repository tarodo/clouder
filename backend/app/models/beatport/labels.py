from pydantic import constr
from sqlmodel import Field, SQLModel

name_con = constr(min_length=1)
url_con = constr(min_length=1)


class LabelBase(SQLModel):
    name: name_con = Field(index=True, nullable=False)
    url: url_con = Field(nullable=False)
    bp_id: int = Field(index=True, nullable=False)


class LabelBaseDB(LabelBase):
    pass


class Label(LabelBaseDB, table=True):
    id: int = Field(primary_key=True)


class LabelInDB(LabelBaseDB):
    pass


class LabelOut(LabelBaseDB):
    id: int = Field(...)


class LabelInApi(LabelBase):
    pass
