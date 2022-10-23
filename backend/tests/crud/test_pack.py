import datetime
import random

from app.crud import packs
from app.models import PackInDB, PackUpdate, User
from sqlmodel import Session
from tests.utils.packs import create_random_pack, create_random_packs
from tests.utils.periods import create_random_period
from tests.utils.styles import create_random_style
from tests.utils.utils import random_lower_string


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
