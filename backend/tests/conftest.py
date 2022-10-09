from typing import Generator

import pytest
from app.db import session
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="session")
def db() -> Generator:
    yield session


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
