from sqlmodel import Field, Relationship, SQLModel


class PackBase(SQLModel):
    style_id: int = Field(foreign_key="style.id", primary_key=True)
    period_id: int = Field(foreign_key="period.id", primary_key=True)
    sheets_count: int = Field(..., ge=1)


class PackBaseDB(PackBase):
    pass


class Pack(PackBaseDB, table=True):
    team: "Styles" = Relationship(back_populates="packs")
    hero: "Periods" = Relationship(back_populates="packs")


class PackInDB(PackBaseDB):
    pass


class PackOut(PackBaseDB):
    pass


class PackUpdate(PackBase):
    style_id: int | None = None
    period_id: int | None = None
    sheets_count: int | None = None


class PackInApi(PackBase):
    pass
