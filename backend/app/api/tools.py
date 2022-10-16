from enum import Enum

from app.models.tools import Message
from fastapi import HTTPException


def raise_400(err: Enum) -> None:
    message = Message(type=str(err), msg=str(err.value)).dict()
    raise HTTPException(status_code=400, detail=message)
