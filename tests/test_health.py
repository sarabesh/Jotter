from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from jotter import __version__
from jotter.db import IdeaStore
from jotter.health import build_health_router


def test_health_ok(client: TestClient) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "version": __version__}


def test_health_503_when_database_unreachable(tmp_path: Path) -> None:
    store = IdeaStore(tmp_path / "test.db")
    store.path = str(tmp_path / "missing-dir" / "test.db")  # sqlite can't create the folder
    app = FastAPI()
    app.include_router(build_health_router(store))

    r = TestClient(app).get("/health")
    assert r.status_code == 503
    assert r.json()["status"] == "error"


def test_health_not_in_api_docs(client: TestClient) -> None:
    assert client.get("/openapi.json").status_code == 404
