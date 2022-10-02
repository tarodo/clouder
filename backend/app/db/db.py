from app.core.config import settings
from sqlmodel import Session, create_engine
from sqlmodel.sql.expression import Select, SelectOfScalar

engine = create_engine(settings.DB_URL, echo=True)
session = Session(bind=engine, expire_on_commit=False)
SelectOfScalar.inherit_cache = True
Select.inherit_cache = True
