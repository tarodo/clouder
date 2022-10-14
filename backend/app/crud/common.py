from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, SQLModel, select


def read_by_id(db: Session, Model, elem_id: int) -> SQLModel | None:
    """Read one element by id"""
    elem = select(Model).where(Model.id == elem_id)
    elem = db.exec(elem).one_or_none()
    return elem


def create(db: Session, Model, payload: SQLModel) -> SQLModel:
    """Create an element"""
    element = Model(**payload.dict())
    db.add(element)
    db.commit()
    db.refresh(element)
    return element


def update(db: Session, db_obj: SQLModel, payload: SQLModel) -> SQLModel:
    """Update style's data"""
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


def remove(db: Session, db_obj: SQLModel) -> SQLModel:
    """Remove style from DB"""
    db.delete(db_obj)
    db.commit()
    return db_obj
