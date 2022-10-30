from app.models.beatport.releases import ReleaseArtist
from pydantic import constr
from sqlmodel import Field, Relationship, SQLModel

name_con = constr(min_length=1, max_length=127)
url_con = constr(min_length=1)


class ArtistBase(SQLModel):
    name: name_con = Field(index=True, nullable=False)
    url: url_con = Field(nullable=False)
    bp_id: int = Field(index=True, nullable=False, sa_column_kwargs={"unique": True})


class ArtistBaseDB(ArtistBase):
    pass


class Artist(ArtistBaseDB, table=True):
    id: int = Field(primary_key=True)

    releases: list["Release"] = Relationship(
        back_populates="artists", link_model=ReleaseArtist
    )


class ArtistInDB(ArtistBaseDB):
    pass


class ArtistOut(ArtistBaseDB):
    id: int = Field(...)


class ArtistInApi(ArtistBase):
    pass
