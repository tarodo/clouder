import datetime
import logging
import math
import random

from app.crud import packs
from app.models import Pack, PackInDB, User, PackInApi
from sqlmodel import Session
from tests.utils.periods import create_random_period, create_random_periods
from tests.utils.styles import create_random_style, create_random_styles


def get_valid_pack_dict(db: Session, user: User, style_id: int | None = None, period_id: int | None = None) -> dict:
    """Return valid dict of random pack"""
    if not style_id:
        style = create_random_style(db, user)
        style_id = style.id
    if not period_id:
        period = create_random_period(db, user)
        period_id = period.id
    return {
        "style_id": style_id,
        "period_id": period_id,
        "sheets_count": random.randint(1, 10),
    }


def get_valid_pack_in(db: Session, user: User, style_id: int | None = None, period_id: int | None = None) -> PackInDB:
    """Return valid random PeriodInApi"""
    return PackInDB(**get_valid_pack_dict(db, user, style_id, period_id))


def create_random_pack(db: Session, user: User, style_id: int | None = None, period_id: int | None = None) -> Pack:
    """Create random pack for the user"""
    pack_in = get_valid_pack_in(db, user, style_id, period_id)
    return packs.create(db, payload=pack_in)


def create_random_packs(
    db: Session, user: User, cnt: int = None, min_cnt: int = 2, max_cnt: int = 10
) -> list[Pack] | None:
    """Create list of packs for the user"""
    if not cnt:
        if min_cnt and max_cnt:
            cnt = random.randint(min_cnt, max_cnt)
        else:
            return None
    styles = create_random_styles(db, user, min_cnt=1, max_cnt=max(1, cnt // 2))
    styles_cnt = len(styles)
    periods_cnt = math.ceil(cnt / styles_cnt)
    periods = create_random_periods(db, user, cnt=periods_cnt)
    random_packs = []
    for style in styles:
        for period in periods:
            pack = PackInDB(
                style_id=style.id,
                period_id=period.id,
                sheets_count=random.randint(1, 10),
            )
            new_pack = packs.create(db, payload=pack)
            random_packs.append(new_pack)
    return random_packs[:cnt]
