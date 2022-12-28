import random

from app.crud.beatport import sessions
from app.models import BPSessionInDB, User
from sqlmodel import Session
from tests.utils.beatport import create_random_release
from tests.utils.periods import create_random_period
from tests.utils.styles import create_random_style


def test_session_create(db: Session, random_user: User) -> None:
    style = create_random_style(db, random_user)
    period = create_random_period(db, random_user)
    session_in = BPSessionInDB(
        style_id=style.id, period_id=period.id, sheets_count=random.randint(1, 10)
    )
    session = sessions.create(db, payload=session_in)
    assert session
    assert session.style_id == session_in.style_id
    assert session.period_id == session_in.period_id
    assert session.sheets_count == session_in.sheets_count