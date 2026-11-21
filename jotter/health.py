"""Health check for Docker HEALTHCHECK and Kubernetes probes (not part of the UI)."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from jotter import __version__
from jotter.db import IdeaStore


def build_health_router(store: IdeaStore) -> APIRouter:
    router = APIRouter(include_in_schema=False)

    @router.get("/health")
    def health() -> JSONResponse:
        """200 {"status": "ok"} when the app can reach its database, else 503."""
        if store.ping():
            return JSONResponse({"status": "ok", "version": __version__})
        return JSONResponse({"status": "error", "version": __version__}, status_code=503)

    return router
