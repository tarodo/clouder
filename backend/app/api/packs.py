from enum import Enum

from app.api import deps
from app.api.beatport.releases import ReleasesErrors
from app.api.tools import raise_400
from app.crud import packs, periods, styles
from app.crud.beatport import releases
from app.models import Pack, PackInApi, PackInDB, PackOut, User, responses
from fastapi import APIRouter, Depends, Path, Query
from sqlmodel import Session

router = APIRouter()


class PacksErrors(Enum):
    PackAlreadyExists = "Pack with Style ID :{}: && Period ID :{}: already exists"
    PackDoesNotExist = "Pack ID :{}: does not exist"
    UserHasNoRights = "User ID :{}: has no rights"
    UserHasNoAccess = "User ID :{}: has no access"
    NotEnoughParams = "Not valid count of query params. Style ID of Period ID must be in your query params"


def check_to_create(db: Session, user: User, one_pack_in: PackInApi) -> bool:
    """Check if the user has 'create' permission"""
    style = styles.read_by_id(db, one_pack_in.style_id)
    if not style or (style.user is not user):
        return False
    period = periods.read_by_id(db, one_pack_in.period_id)
    if not period or (period.user is not user):
        return False
    return True


def check_to_read_by_style_period(
    db: Session, user: User, style_id: int | None = None, period_id: int | None = None
) -> bool:
    """Check if the user has read permission"""
    if style_id:
        one_style = styles.read_by_id(db, style_id)
        if not one_style:
            return False
        if one_style.user is not user:
            return False
    if period_id:
        one_period = periods.read_by_id(db, period_id)
        if not one_period:
            return False
        if one_period.user is not user:
            return False
    return True


def check_to_read(user: User, one_pack: Pack) -> bool:
    """Check if the user has 'read' permission"""
    if user.is_admin:
        return True
    one_style = one_pack.style
    one_period = one_pack.period
    if user is one_style.user and user is one_period.user:
        return True
    return False


def check_to_remove(user: User, one_pack: Pack) -> bool:
    """Check if the user has 'delete' permission"""
    return check_to_read(user, one_pack)


def create_pack_out(q_pack: Pack) -> PackOut:
    """Collect releases for a pack"""
    pack_releases = [pr.release for pr in q_pack.pack_releases]
    return PackOut(**q_pack.dict(), releases=pack_releases)


@router.post("/", response_model=PackOut, status_code=200, responses=responses)
def create_pack(
    payload: PackInApi,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Pack:
    """Create one pack"""
    old_pack = packs.read_packs(db, payload.style_id, payload.period_id)
    if old_pack:
        raise_400(PacksErrors.PackAlreadyExists, payload.style_id, payload.period_id)
    if not check_to_create(db, current_user, payload):
        raise_400(PacksErrors.UserHasNoRights, current_user.id)
    pack_in = PackInDB(**payload.dict())
    pack = packs.create(db, pack_in)
    return pack


@router.get("/", response_model=list[PackOut], status_code=200, responses=responses)
def read_many(
    style_id: int | None = Query(None, ge=1),
    period_id: int | None = Query(None, ge=1),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> list[PackOut] | None:
    """Retrieve all packs for style and period"""
    if not style_id and not period_id:
        raise_400(PacksErrors.NotEnoughParams)
    if not current_user.is_admin:
        if not check_to_read_by_style_period(db, current_user, style_id, period_id):
            raise_400(PacksErrors.UserHasNoAccess, current_user.id)
    query_packs = packs.read_packs(db, style_id, period_id)
    packs_out = [create_pack_out(one_pack) for one_pack in query_packs]
    return packs_out


@router.get("/{pack_id}/", response_model=PackOut, status_code=200, responses=responses)
def read(
    pack_id: int = Path(..., gt=0),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> PackOut | None:
    """Retrieve a pack by id"""
    one_pack = packs.read_by_id(db, pack_id)
    if one_pack:
        if check_to_read(current_user, one_pack):
            return create_pack_out(one_pack)
    else:
        if current_user.is_admin:
            return raise_400(PacksErrors.PackDoesNotExist, pack_id)
    return raise_400(PacksErrors.UserHasNoAccess, current_user.id)


@router.delete(
    "/{pack_id}/", response_model=PackOut, status_code=200, responses=responses
)
def remove(
    pack_id: int = Path(..., gt=0),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Pack | None:
    """Remove the pack by id"""
    one_pack = packs.read_by_id(db, pack_id)
    if not one_pack:
        if current_user.is_admin:
            return raise_400(PacksErrors.PackDoesNotExist, pack_id)
        return raise_400(PacksErrors.UserHasNoRights, current_user.id)
    if not check_to_remove(current_user, one_pack):
        return raise_400(PacksErrors.UserHasNoRights, current_user.id)

    return packs.remove(db, one_pack)


@router.post(
    "/{pack_id}/releases/{release_id}",
    response_model=PackOut,
    status_code=200,
    responses=responses,
)
def add_release(
    pack_id: int = Path(..., gt=0),
    release_id: int = Path(..., gt=0),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> PackOut | None:
    """Add one release to a pack"""
    one_pack = packs.read_by_id(db, pack_id)
    if not one_pack:
        if current_user.is_admin:
            return raise_400(PacksErrors.PackDoesNotExist, pack_id)
        else:
            return raise_400(PacksErrors.UserHasNoAccess, current_user.id)
    if not check_to_read(current_user, one_pack):
        return raise_400(PacksErrors.UserHasNoAccess, current_user.id)

    one_release = releases.read_by_id(db, release_id)
    if not one_release:
        raise_400(ReleasesErrors.ReleaseDoesNotExist, release_id)

    new_pack = packs.add_release(db, one_pack, one_release)
    return create_pack_out(new_pack)
