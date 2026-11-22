# jotter

A tiny web app for capturing ideas: jot one down, add details and tags, come back to it later. Planned features are in [BACKLOG.md](BACKLOG.md).

## Pages
| Page | What |
|---|---|
| `/` | Your ideas, newest first (empty state when there are none) |
| `/new` | Add an idea (title, optional details, comma-separated tags) |
| `/ideas/{id}` | Read an idea; edit or delete it |
| `/ideas/{id}/edit` | Edit an idea |
| `/health` | `{"status": "ok", "version": "…"}` for Docker/k8s health checks; 503 if the database can't be reached |

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

## Releases
[`.github/workflows/release.yml`](.github/workflows/release.yml) runs on every push to `main`:

1. **release-please** reads the [Conventional Commit](https://www.conventionalcommits.org/) messages since the last release and keeps one open **release PR** (version bump in `pyproject.toml`, `uv.lock`, `jotter/__init__.py`, plus `CHANGELOG.md`).
2. **Merging the release PR** tags `vX.Y.Z`, creates a GitHub Release and publishes the image:
   build → trivy gate (HIGH/CRITICAL) → push `ghcr.io/sarabesh/jotter:X.Y.Z` → cosign keyless signature → CycloneDX SBOM attestation → verify → SBOM attached to the release.
3. **deploy-staging** clones [jotter-deploy](https://github.com/sarabesh/jotter-deploy), sets `overlays/staging` to `X.Y.Z`, commits `deploy(staging): jotter X.Y.Z` and pushes to its `main` (SSH deploy key, secret `JOTTER_DEPLOY_KEY`). Argo CD then deploys staging. Prod stays a human PR in jotter-deploy.

| PR title (squash merge) | Release |
|---|---|
| `fix: …`, `perf: …`, `deps: …` | patch (0.3.0 → 0.3.1) |
| `feat: …` | minor (0.3.0 → 0.4.0) |
| `feat!: …` / `BREAKING CHANGE:` | minor while < 1.0 |
| `ci:`, `docs:`, `chore:`, `test:`, `refactor:` | no release |

Verify a published image:
```bash
cosign verify ghcr.io/sarabesh/jotter:<version> \
  --certificate-identity https://github.com/sarabesh/Jotter/.github/workflows/release.yml@refs/heads/main \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

## Docker
```bash
docker build -t jotter .
docker run --rm -p 8000:8000 -v jotter-data:/data jotter
```
