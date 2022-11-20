import random

from app.crud import packs
from app.models import PackInDB, PackReleaseInDB, User
from sqlmodel import Session
from tests.utils.beatport import create_random_release
from tests.utils.packs import create_random_pack, create_random_packs
from tests.utils.periods import create_random_period
from tests.utils.styles import create_random_style


def test_pack_create(db: Session, random_user: User) -> None:
    style = create_random_style(db, random_user)
    period = create_random_period(db, random_user)
    pack_in = PackInDB(
        style_id=style.id, period_id=period.id, sheets_count=random.randint(1, 10)
    )
    pack = packs.create(db, payload=pack_in)
    assert pack
    assert pack.style_id == pack_in.style_id
    assert pack.period_id == pack_in.period_id
    assert pack.sheets_count == pack_in.sheets_count


def test_pack_read(db: Session, random_user: User) -> None:
    pack = create_random_pack(db, random_user)
    test_packs = packs.read_packs(db, pack.style_id, pack.period_id)
    assert test_packs[0] == pack


def test_pack_read_by_style(db: Session, random_user: User) -> None:
    user_packs = create_random_packs(db, random_user, 8)
    control_style = user_packs[0].style_id
    test_packs = packs.read_packs(db, style_id=control_style)
    assert test_packs
    assert all(pack in user_packs for pack in test_packs)


def test_pack_read_by_period(db: Session, random_user: User) -> None:
    user_packs = create_random_packs(db, random_user, 8)
    control_period = user_packs[0].period_id
    test_packs = packs.read_packs(db, period_id=control_period)
    assert test_packs
    assert all(pack in user_packs for pack in test_packs)


def test_pack_release_create(db: Session, random_user: User) -> None:
    pack = create_random_pack(db, random_user)
    release = create_random_release(db)
    pack_release = packs.add_release(db, pack, release)
    assert pack_release
    assert pack_release.release == release
    assert pack_release.pack == pack
    assert not pack_release.audited


def test_pack_release_read(db: Session, random_user: User) -> None:
    pack = create_random_pack(db, random_user)
    release = create_random_release(db)
    pack_release_control = packs.add_release(db, pack, release)
    assert pack_release_control
    pack_release = packs.read_pack_release(db, pack, release)
    assert pack_release
    assert pack_release == pack_release_control


def test_pack_release_make_audited(db: Session, random_user: User) -> None:
    pack = create_random_pack(db, random_user)
    release = create_random_release(db)
    pack_release = packs.add_release(db, pack, release)
    assert pack_release
    assert not pack_release.audited
    pack_release = packs.make_audited(db, pack_release)
    assert pack_release
    assert pack_release.audited
