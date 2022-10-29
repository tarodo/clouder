import logging
from enum import Enum

from app.api import deps
from app.api.tools import raise_400
from app.crud.beatport import labels
from app.models import Label, LabelInApi, LabelInDB, LabelOut, User, responses
from app.models.beatport.labels import name_con
from fastapi import APIRouter, Body, Depends, Query
from pydantic import ValidationError
from sqlmodel import Session

router = APIRouter()


class LabelsErrors(Enum):
    LabelAlreadyExists = "Label already exists"
    LabelDoesNotExist = "Label does not exist"
    UserHasNoRights = "User has no rights"


create_examples = {}


@router.post("/", response_model=LabelOut, status_code=200, responses=responses)
def create_label(
    payload: LabelInApi = Body(examples=create_examples),
    _: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Label:
    """Create one label"""
    old_label = labels.read_by_bp_id(db, payload.bp_id)
    if old_label:
        raise_400(LabelsErrors.LabelAlreadyExists)
    label_in = LabelInDB(**payload.dict())
    label = labels.create(db, label_in)
    return label


@router.get(
    "/findByName", response_model=list[LabelOut], status_code=200, responses=responses
)
def read_many(
    name: str
    | None = Query(
        None, min_length=name_con.min_length, max_length=name_con.max_length
    ),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> list[Label] | None:
    """Retrieve labels by name"""
    return labels.read_by_name(db, name)


@router.get(
    "/findByBpId", response_model=LabelOut, status_code=200, responses=responses
)
def read_many(
    bp_id: int | None = Query(None, ge=1),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> list[Label] | None:
    """Retrieve one label by beatport ID"""
    return labels.read_by_bp_id(db, bp_id)


@router.get(
    "/{label_id}/", response_model=LabelOut, status_code=200, responses=responses
)
def read(
    label_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Label | None:
    """Retrieve a label by id"""
    one_label = labels.read_by_id(db, label_id)
    if not one_label:
        raise_400(LabelsErrors.LabelDoesNotExist)
    return one_label


@router.delete(
    "/{label_id}/", response_model=LabelOut, status_code=200, responses=responses
)
def remove(
    label_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Label | None:
    """Remove the label by id. Only admin can delete a label."""
    if not current_user.is_admin:
        raise_400(LabelsErrors.UserHasNoRights)
    one_label = labels.read_by_id(db, label_id)
    if not one_label:
        raise_400(LabelsErrors.LabelDoesNotExist)
    return labels.remove(db, one_label)
