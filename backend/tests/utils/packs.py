import datetime
import logging
import math
import random

from app.crud import packs
from app.models import Pack, PackInApi, PackInDB, User
from sqlmodel import Session
from tests.utils.periods import create_random_period, create_random_periods
from tests.utils.styles import create_random_style, create_random_styles
from tests.utils.utils import random_date, random_lower_string


def create_random_pack(db: Session, user: User) -> Pack:
    """Create random pack for the user"""
    style = create_random_style(db, user)
    period = create_random_period(db, user)
    pack_in = PackInDB(
        style_id=style.id, period_id=period.id, sheets_count=random.randint(1, 10)
    )
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
    logging.error(f"{cnt=} :: {styles_cnt=} :: {periods_cnt=}")
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
            logging.error(f"{new_pack=}")
            random_packs.append(new_pack)
    return random_packs[:cnt]
