"""App factory: the web app (HTML pages) plus its stylesheet.

Run locally:
    uv run uvicorn jotter.main:create_app --factory --reload
"""

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from jotter import __version__
from jotter.db import IdeaStore
from jotter.web import build_web_router

STATIC_DIR = Path(__file__).parent / "static"


def create_app(db_path: str | Path | None = None) -> FastAPI:
    """Build the app. Database path: argument, else $JOTTER_DB, else ./jotter.db."""
    store = IdeaStore(db_path or os.environ.get("JOTTER_DB", "jotter.db"))

    # No public API, so no auto-generated API docs pages either.
    app = FastAPI(
        title="jotter", version=__version__, docs_url=None, redoc_url=None, openapi_url=None
    )

    app.include_router(build_web_router(store))
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    return app
