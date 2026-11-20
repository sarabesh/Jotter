# AGENTS.md

Instructions for coding agents (and humans) working on this repo.

## What this is
`jotter` — a tiny web app for capturing ideas. Server-rendered HTML pages, no public API. FastAPI + Jinja2 + SQLite (standard library `sqlite3`), Python 3.12.

## Layout
- `jotter/main.py` — app factory `create_app()`; mounts the pages and `/static` (API docs pages are turned off)
- `jotter/web.py` — all routes (`/`, `/new`, `/ideas/{id}`, edit, delete) using HTML forms + redirects
- `jotter/templates/` — Jinja2 templates (`base.html`, `index.html`, `idea.html`, `form.html`)
- `jotter/static/style.css` — the only stylesheet (CSS variables, light/dark mode)
- `jotter/db.py` — `IdeaStore`, the only place that touches SQLite (table `ideas`)
- `tests/test_web.py` — page tests; `client` fixture in `tests/conftest.py` gives a fresh database per test

## Commands
```bash
uv sync                        # install
uv run pytest                  # tests (must pass)
uv run ruff check .            # lint (must pass)
uv run ruff format --check .   # formatting (must pass; fix with `uv run ruff format .`)
uv run mypy                    # types, strict (must pass)
uv run uvicorn jotter.main:create_app --factory --reload   # run locally on :8000
```

## Conventions
- Keep it simple: no new dependencies unless the task needs them; say why if you add one.
- All SQL goes in `jotter/db.py` and always uses `?` parameters — never build SQL with f-strings or `+`.
- Every behavior change comes with a test in `tests/`.
- Type hints everywhere (mypy strict).
- Pages: no JavaScript frameworks or build step; plain HTML forms, POST → 303 redirect (Post/Redirect/Get). Validation errors re-show the form with a message and keep what the user typed.
- Never mark user content `| safe` in templates (autoescaping protects against XSS).
- Missing ideas raise `HTTPException(404)`.
- Commit messages follow Conventional Commits (`feat: …`, `fix: …`, `test: …`).

## Don't touch
`.github/`, `tests/acceptance/` (hidden acceptance tests, if present), lint/type config in `pyproject.toml`.
