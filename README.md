# jotter

A tiny web app for capturing ideas: jot one down, add details and tags, come back to it later. It's the target app the `cda` coding agent works on; features are added from [BACKLOG.md](BACKLOG.md).

## Pages
| Page | What |
|---|---|
| `/` | Your ideas, newest first (empty state when there are none) |
| `/new` | Add an idea (title, optional details, comma-separated tags) |
| `/ideas/{id}` | Read an idea; edit or delete it |
| `/ideas/{id}/edit` | Edit an idea |

Server-rendered HTML (FastAPI + Jinja2 templates + one CSS file), plain HTML forms, no JavaScript build, light and dark mode. Data is stored in SQLite.

## Run
```bash
uv sync
uv run uvicorn jotter.main:create_app --factory --reload
```
Open http://localhost:8000.

## Test
```bash
uv run pytest && uv run ruff check . && uv run ruff format --check . && uv run mypy
```

## CI
[`.github/workflows/pr-gates.yml`](.github/workflows/pr-gates.yml) runs on every PR to `main` and on `main` itself. Four parallel checks:

| Check | What it runs |
|---|---|
| `lint (ruff)` | `uv sync --locked`, `ruff check`, `ruff format --check` |
| `types (mypy)` | `mypy` (strict) |
| `test (pytest)` | `pytest` with coverage report |
| `docker (build + smoke test)` | builds the image, starts it, checks the home page loads |

## Docker
```bash
docker build -t jotter .
docker run --rm -p 8000:8000 -v jotter-data:/data jotter
```
