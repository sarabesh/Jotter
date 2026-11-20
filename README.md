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
[`.github/workflows/pr-gates.yml`](.github/workflows/pr-gates.yml) runs on every PR to `main` and on `main` itself. All checks run in parallel and are required to merge:

| Check | What it runs |
|---|---|
| `lint (ruff)` | `uv sync --locked`, `ruff check` (incl. bandit security rules), `ruff format --check` |
| `types (mypy)` | `mypy` (strict) |
| `test (pytest)` | `pytest`, fails below 90% coverage |
| `docker (build + smoke test)` | builds the image, starts it, checks the home page loads |
| `secrets (gitleaks)` | scans every commit in the PR for leaked keys/passwords |
| `sast (semgrep)` | static security analysis (`p/python` rules) |
| `deps (pip-audit + licences)` | known CVEs in locked dependencies; runtime dependency licences (no GPL family) |
| `image scan (trivy + SBOM)` | HIGH/CRITICAL fixable CVEs in the Docker image; CycloneDX SBOM uploaded as an artifact |

## Docker
```bash
docker build -t jotter .
docker run --rm -p 8000:8000 -v jotter-data:/data jotter
```
