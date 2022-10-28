from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import InstrumentedAttribute
from sqlmodel import Session, SQLModel, select


def read_by_id(db: Session, Model, elem_id: int) -> SQLModel | None:
    """Read one element by id"""
    elem = select(Model).where(Model.id == elem_id)
    elem = db.exec(elem).one_or_none()
    return elem


def read_by_field(db: Session, Field: InstrumentedAttribute, value) -> SQLModel | None:
    """Read element by field value"""
    elem = select(Field.class_).where(Field == value)
    elem = db.exec(elem).one_or_none()
    return elem


def create(db: Session, Model, payload: SQLModel):
    """Create an element"""
    element = Model(**payload.dict())
    db.add(element)
    db.commit()
    db.refresh(element)
    return element


def update(db: Session, db_obj: SQLModel, payload: SQLModel):
    """Update element's data"""
    obj_data = jsonable_encoder(db_obj)
    update_data = payload.dict(exclude_unset=True, exclude_none=True)
    for field in obj_data:
        if field in update_data:
            new_data = update_data[field]
            setattr(db_obj, field, new_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, db_obj: SQLModel):
    """Remove element from DB"""
    db.delete(db_obj)
    db.commit()
    return db_obj
