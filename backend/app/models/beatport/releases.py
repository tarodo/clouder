from app.models.beatport.labels import Label
from pydantic import constr
from sqlmodel import Field, Relationship, SQLModel

name_con = constr(min_length=1, max_length=127)
url_con = constr(min_length=1)


class ReleaseArtist(SQLModel, table=True):
    release_id: int = Field(default=None, foreign_key="release.id", primary_key=True)
    artist_id: int = Field(default=None, foreign_key="artist.id", primary_key=True)


class ReleaseBase(SQLModel):
    name: name_con = Field(index=True, nullable=False)
    url: url_con = Field(nullable=False)
    bp_id: int = Field(index=True, nullable=False, sa_column_kwargs={"unique": True})
    label_id: int = Field(foreign_key="label.id")


class ReleaseBaseDB(ReleaseBase):
    pass


class Release(ReleaseBaseDB, table=True):
    id: int = Field(primary_key=True)

    label: Label = Relationship(back_populates="releases")
    artists: list["Artist"] = Relationship(
        back_populates="releases", link_model=ReleaseArtist
    )


class ReleaseInDB(ReleaseBaseDB):
    pass


class ReleaseOut(ReleaseBaseDB):
    id: int = Field(...)


class ReleaseInApi(ReleaseBase):
    pass
