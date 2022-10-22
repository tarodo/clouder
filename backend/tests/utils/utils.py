import random
import string
import time
from datetime import datetime


def random_lower_string(str_len: int = 32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=str_len))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string(8)}.com"


def random_date(start_date: int = 1, end_date: int = None) -> datetime:
    # TODO: Change inputs to datetime
    if not end_date:
        end_date = int(time.time())
    new_date = random.randint(start_date, end_date)
    return datetime.fromtimestamp(new_date)
