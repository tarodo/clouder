from enum import Enum

from app.api import deps
from app.api.tools import raise_400
from app.crud.beatport import artists, labels, releases
from app.models import (Release, ReleaseInApi, ReleaseInDB, ReleaseOut, User,
                        responses)
from app.models.beatport.releases import name_con
from fastapi import APIRouter, Body, Depends, Path, Query
from sqlmodel import Session

router = APIRouter()


class ReleasesErrors(Enum):
    ReleaseAlreadyExists = "Release already exists"
    ReleaseDoesNotExist = "Release ID :{}: does not exist"
    UserHasNoRights = "User ID :{}: has no rights"
    ArtistDoesNotExists = "Artist ID :{}: does not exist"
    LabelDoesNotExists = "Label ID :{}: does not exist"


@router.post("/", response_model=ReleaseOut, status_code=200, responses=responses)
def create_release(
    payload: ReleaseInApi = Body(),
    _: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Release:
    """Create one release"""
    if payload.label_id:
        q_label = labels.read_by_id(db, payload.label_id)
        if not q_label:
            raise_400(ReleasesErrors.LabelDoesNotExists, payload.label_id)

    q_artists = []
    if payload.artists_id:
        for art_id in payload.artists_id:
            art_db = artists.read_by_id(db, art_id)
            if not art_db:
                raise_400(ReleasesErrors.ArtistDoesNotExists, art_id)
            q_artists.append(art_db)
    release_in = ReleaseInDB(**payload.dict())
    return releases.create(db, release_in, q_artists)


@router.get(
    "/findByName", response_model=list[ReleaseOut], status_code=200, responses=responses
)
def read_many_by_name(
    name: name_con = Query(...),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> list[Release] | None:
    """Retrieve releases by name"""
    return releases.read_by_name(db, name)


@router.get(
    "/findByBpId", response_model=ReleaseOut, status_code=200, responses=responses
)
def read_many_by_bp_id(
    bp_id: int | None = Query(None, ge=1),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> list[Release] | None:
    """Retrieve one release by beatport ID"""
    return releases.read_by_bp_id(db, bp_id)


@router.get(
    "/findByLabelId",
    response_model=list[ReleaseOut],
    status_code=200,
    responses=responses,
)
def read_many_by_label(
    label_id: int | None = Query(None, ge=1),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> list[Release] | None:
    """Retrieve all releases by Label ID"""
    q_label = labels.read_by_id(db, label_id)
    if not q_label:
        raise_400(ReleasesErrors.LabelDoesNotExists, label_id)
    q_releases = releases.read_by_label_id(db, q_label)
    return q_releases


@router.get(
    "/findByArtistId",
    response_model=list[ReleaseOut],
    status_code=200,
    responses=responses,
)
def read_many(
    artist_id: int | None = Query(None, ge=1),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> list[Release] | None:
    """Retrieve all releases by Artist ID"""
    q_artist = artists.read_by_id(db, artist_id)
    if not q_artist:
        raise_400(ReleasesErrors.ArtistDoesNotExists, artist_id)
    q_releases = releases.read_by_artist(db, q_artist)
    return q_releases


@router.get(
    "/{release_id}/", response_model=ReleaseOut, status_code=200, responses=responses
)
def read(
    release_id: int = Path(..., gt=0),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Release | None:
    """Retrieve a release by id"""
    one_release = releases.read_by_id(db, release_id)
    if not one_release:
        raise_400(ReleasesErrors.ReleaseDoesNotExist, release_id)
    return one_release


@router.delete(
    "/{release_id}/", response_model=ReleaseOut, status_code=200, responses=responses
)
def remove(
    release_id: int = Path(..., gt=0),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Release | None:
    """Remove the release by id. Only admin can delete a release."""
    if not current_user.is_admin:
        raise_400(ReleasesErrors.UserHasNoRights, current_user.id)
    one_release = releases.read_by_id(db, release_id)
    if not one_release:
        raise_400(ReleasesErrors.ReleaseDoesNotExist, release_id)
    return releases.remove(db, one_release)
