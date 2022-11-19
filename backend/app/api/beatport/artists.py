from enum import Enum

from app.api import deps
from app.api.tools import raise_400
from app.crud.beatport import artists
from app.models import (Artist, ArtistInApi, ArtistInDB, ArtistOut, User,
                        responses)
from app.models.beatport.artists import name_con
from fastapi import APIRouter, Body, Depends, Path, Query
from sqlmodel import Session

router = APIRouter()


class ArtistsErrors(Enum):
    ArtistAlreadyExists = "Artist already exists"
    ArtistDoesNotExist = "Artist does not exist"
    UserHasNoRights = "User has no rights"


create_examples = {}


@router.post("/", response_model=ArtistOut, status_code=200, responses=responses)
def create_artist(
    payload: ArtistInApi = Body(examples=create_examples),
    _: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Artist:
    """Create one artist"""
    old_artist = artists.read_by_bp_id(db, payload.bp_id)
    if old_artist:
        raise_400(ArtistsErrors.ArtistAlreadyExists)
    artist_in = ArtistInDB(**payload.dict())
    artist = artists.create(db, artist_in)
    return artist


@router.get(
    "/findByName", response_model=list[ArtistOut], status_code=200, responses=responses
)
def read_many(
    name: name_con = Query(...),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> list[Artist] | None:
    """Retrieve artists by name"""
    return artists.read_by_name(db, name)


@router.get(
    "/findByBpId", response_model=ArtistOut, status_code=200, responses=responses
)
def read_many(
    bp_id: int | None = Query(None, ge=1),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> list[Artist] | None:
    """Retrieve one artist by beatport ID"""
    return artists.read_by_bp_id(db, bp_id)


@router.get(
    "/{artist_id}/", response_model=ArtistOut, status_code=200, responses=responses
)
def read(
    artist_id: int = Path(..., gt=0),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Artist | None:
    """Retrieve a artist by id"""
    one_artist = artists.read_by_id(db, artist_id)
    if not one_artist:
        raise_400(ArtistsErrors.ArtistDoesNotExist)
    return one_artist


@router.delete(
    "/{artist_id}/", response_model=ArtistOut, status_code=200, responses=responses
)
def remove(
    artist_id: int = Path(..., gt=0),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Artist | None:
    """Remove the artist by id. Only admin can delete an artist."""
    if not current_user.is_admin:
        raise_400(ArtistsErrors.UserHasNoRights)
    one_artist = artists.read_by_id(db, artist_id)
    if not one_artist:
        raise_400(ArtistsErrors.ArtistDoesNotExist)
    return artists.remove(db, one_artist)
