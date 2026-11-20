from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from jotter.main import create_app


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    """A client backed by a fresh database for every test."""
    return TestClient(create_app(tmp_path / "test.db"))
