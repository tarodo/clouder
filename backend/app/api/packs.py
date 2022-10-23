from enum import Enum

from app.api import deps
from app.api.tools import raise_400
from app.crud import packs
from app.models import (Pack, PackInApi, PackInDB, PackOut, PackUpdate, User,
                        responses)
from fastapi import APIRouter, Body, Depends
from pydantic import ValidationError
from sqlmodel import Session

router = APIRouter()


class PacksErrors(Enum):
    pass


def check_to_read(user: User, one_pack: Pack) -> bool:
    """Check if the user has read permission"""
    pass


def check_to_update(user: User, one_pack: Pack) -> bool:
    """Check if the user has update permission"""
    pass


def check_to_remove(user: User, one_pack: Pack) -> bool:
    """Check if the user has delete permission"""
    pass


create_examples = {}

update_example = {}


@router.post("/", response_model=PackOut, status_code=200, responses=responses)
def create_pack(
    payload: PackInApi = Body(examples=create_examples),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Pack:
    """Create one pack"""
    pass


@router.get("/", response_model=list[PackOut], status_code=200, responses=responses)
def read_my(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> list[Pack] | None:
    """Retrieve all packs for the user"""
    pass


@router.get("/{pack_id}/", response_model=PackOut, status_code=200, responses=responses)
def read(
    pack_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Pack | None:
    """Retrieve a pack by id"""
    pass


@router.put("/{pack_id}/", response_model=PackOut, status_code=200, responses=responses)
def update(
    pack_id: int,
    payload: PackUpdate = Body(examples=update_example),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Pack | None:
    """Update the pack for the user"""
    pass


@router.delete(
    "/{pack_id}/", response_model=PackOut, status_code=200, responses=responses
)
def remove(
    pack_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Pack | None:
    """Remove the pack by id"""
    pass
