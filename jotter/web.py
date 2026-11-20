"""Browser UI: server-rendered HTML pages on top of the same IdeaStore."""

from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from jotter.db import IdeaStore

TEMPLATES_DIR = Path(__file__).parent / "templates"
MISSING_TITLE = "Give your idea a short title."


def nice_date(iso: str) -> str:
    """'2026-11-20T14:32:05+00:00' -> 'Nov 20, 2026'."""
    return datetime.fromisoformat(iso).strftime("%b %d, %Y").replace(" 0", " ")


def parse_tags(raw: str) -> list[str]:
    """'work, app ,,fun' -> ['work', 'app', 'fun']."""
    return [t.strip() for t in raw.split(",") if t.strip()]


def build_web_router(store: IdeaStore) -> APIRouter:
    templates = Jinja2Templates(directory=TEMPLATES_DIR)
    templates.env.filters["nice_date"] = nice_date
    router = APIRouter(include_in_schema=False)

    def get_or_404(idea_id: int) -> dict[str, object]:
        idea = store.get(idea_id)
        if idea is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Idea not found")
        return idea

    def form_page(request: Request, idea: Mapping[str, object] | None, error: str = "") -> Response:
        return templates.TemplateResponse(
            request,
            "form.html",
            {"idea": idea, "error": error},
            status_code=status.HTTP_400_BAD_REQUEST if error else status.HTTP_200_OK,
        )

    def go(url: str) -> RedirectResponse:
        return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)

    @router.get("/")
    def home(request: Request) -> Response:
        return templates.TemplateResponse(request, "index.html", {"ideas": store.list_all()})

    @router.get("/new")
    def new_idea(request: Request) -> Response:
        return form_page(request, None)

    @router.post("/new")
    def create_idea(
        request: Request,
        title: Annotated[str, Form()] = "",
        body: Annotated[str, Form()] = "",
        tags: Annotated[str, Form()] = "",
    ) -> Response:
        if not title.strip():
            draft = {"title": title, "body": body, "tags": parse_tags(tags)}
            return form_page(request, draft, MISSING_TITLE)
        idea = store.create(title.strip(), body, parse_tags(tags))
        return go(f"/ideas/{idea['id']}")

    @router.get("/ideas/{idea_id}")
    def show_idea(request: Request, idea_id: int) -> Response:
        return templates.TemplateResponse(request, "idea.html", {"idea": get_or_404(idea_id)})

    @router.get("/ideas/{idea_id}/edit")
    def edit_idea(request: Request, idea_id: int) -> Response:
        return form_page(request, get_or_404(idea_id))

    @router.post("/ideas/{idea_id}/edit")
    def save_idea(
        request: Request,
        idea_id: int,
        title: Annotated[str, Form()] = "",
        body: Annotated[str, Form()] = "",
        tags: Annotated[str, Form()] = "",
    ) -> Response:
        existing = get_or_404(idea_id)
        if not title.strip():
            draft = existing | {"title": title, "body": body, "tags": parse_tags(tags)}
            return form_page(request, draft, MISSING_TITLE)
        store.update(idea_id, title.strip(), body, parse_tags(tags))
        return go(f"/ideas/{idea_id}")

    @router.post("/ideas/{idea_id}/delete")
    def remove_idea(idea_id: int) -> Response:
        get_or_404(idea_id)
        store.delete(idea_id)
        return go("/")

    return router
