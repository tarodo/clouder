from app.models.beatport.artists import Artist, ArtistOut, ReleaseArtist
from app.models.beatport.labels import Label, LabelOut
from pydantic import constr
from sqlmodel import Field, Relationship, SQLModel

name_con = constr(min_length=1, max_length=127)
url_con = constr(min_length=1)


class ReleaseBase(SQLModel):
    name: name_con = Field(index=True, nullable=False)
    url: url_con = Field(nullable=False)
    bp_id: int = Field(index=True, nullable=False, sa_column_kwargs={"unique": True})


class ReleaseBaseDB(ReleaseBase):
    label_id: int | None = Field(foreign_key="label.id")


class Release(ReleaseBaseDB, table=True):
    id: int = Field(primary_key=True)

    label: Label | None = Relationship(back_populates="releases")
    artists: list[Artist] | None = Relationship(
        back_populates="releases", link_model=ReleaseArtist
    )

    pack_releases: list["PackRelease"] = Relationship(back_populates="release")


class ReleaseInDB(ReleaseBaseDB):
    pass


class ReleaseOut(ReleaseBase):
    id: int = Field(...)
    label: LabelOut | None
    artists: list[ArtistOut] | None


class ReleaseInApi(ReleaseBase):
    artists_id: list[int] | None
    label_id: int | None
