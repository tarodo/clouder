from app.models import Release
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

    pack_releases: list["PackRelease"] = Relationship(back_populates="pack")


class PackInDB(PackBaseDB):
    pass


class PackOut(PackBaseDB):
    id: int = Field(...)
    releases: list[Release] = Field(default=[])


class PackInApi(PackBase):
    pass


class PackReleaseBase(SQLModel):
    pack_id: int = Field(foreign_key="pack.id", primary_key=True)
    release_id: int = Field(foreign_key="release.id", primary_key=True)
    audited: bool = Field(nullable=False, default=False)


class PackReleaseBaseDB(PackReleaseBase):
    pass


class PackRelease(PackReleaseBaseDB, table=True):
    pack: Pack | None = Relationship(back_populates="pack_releases")
    release: Release | None = Relationship(back_populates="pack_releases")


class PackReleaseInDB(PackReleaseBaseDB):
    pass


class PackReleaseOut(PackReleaseBaseDB):
    pass


class PackReleaseInApi(PackReleaseBase):
    pass


class PackReleaseUpdate(PackReleaseInApi):
    pass
