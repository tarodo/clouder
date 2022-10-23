from app.models.periods import Period
from app.models.styles import Style
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel


class PackBase(SQLModel):
    style_id: int = Field(foreign_key="style.id")
    period_id: int = Field(foreign_key="period.id")
    sheets_count: int = Field(..., ge=1)


class PackBaseDB(PackBase):
    pass


class Pack(PackBaseDB, table=True):
    __table_args__ = (UniqueConstraint("style_id", "period_id"),)
    id: int = Field(primary_key=True)

    style: Style = Relationship(back_populates="packs")
    period: Period = Relationship(back_populates="packs")


class PackInDB(PackBaseDB):
    pass


class PackOut(PackBaseDB):
    id: int = Field(...)


class PackUpdate(PackBase):
    style_id: int | None = None
    period_id: int | None = None
    sheets_count: int | None = None


class PackInApi(PackBase):
    pass
