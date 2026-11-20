FROM python:3.12-slim

# Apply Debian security fixes released after the base image was built
# (e.g. zlib1g CVE-2026-85091, caught by the trivy image scan). Clean the apt lists to keep the image small.
RUN apt-get update \
 && apt-get upgrade -y --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never \
    PYTHONUNBUFFERED=1 JOTTER_DB=/data/jotter.db

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY jotter/ jotter/

RUN useradd --uid 10001 --create-home app && mkdir /data && chown app /data
USER app
EXPOSE 8000
VOLUME ["/data"]

CMD ["/app/.venv/bin/uvicorn", "jotter.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
