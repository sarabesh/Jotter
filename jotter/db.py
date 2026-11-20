"""SQLite storage for ideas."""

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS ideas (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT NOT NULL,
    body       TEXT NOT NULL,
    tags       TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL
)
"""


def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    idea = dict(row)
    idea["tags"] = json.loads(idea["tags"])
    return idea


class IdeaStore:
    """All database access lives here."""

    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        with self._conn() as conn:
            conn.execute(SCHEMA)

    @contextmanager
    def _conn(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        try:
            with conn:  # commits on success, rolls back on error
                yield conn
        finally:
            conn.close()

    def create(self, title: str, body: str, tags: list[str]) -> dict[str, Any]:
        created_at = datetime.now(UTC).isoformat()
        with self._conn() as conn:
            cur = conn.execute(
                "INSERT INTO ideas (title, body, tags, created_at) VALUES (?, ?, ?, ?)",
                (title, body, json.dumps(tags), created_at),
            )
            idea_id = cur.lastrowid
        assert idea_id is not None  # noqa: S101 - sqlite always sets it after INSERT
        idea = self.get(idea_id)
        assert idea is not None  # noqa: S101
        return idea

    def list_all(self) -> list[dict[str, Any]]:
        with self._conn() as conn:
            rows = conn.execute("SELECT * FROM ideas ORDER BY id DESC").fetchall()
        return [_row_to_dict(r) for r in rows]

    def get(self, idea_id: int) -> dict[str, Any] | None:
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM ideas WHERE id = ?", (idea_id,)).fetchone()
        return _row_to_dict(row) if row else None

    def update(self, idea_id: int, title: str, body: str, tags: list[str]) -> dict[str, Any] | None:
        with self._conn() as conn:
            cur = conn.execute(
                "UPDATE ideas SET title = ?, body = ?, tags = ? WHERE id = ?",
                (title, body, json.dumps(tags), idea_id),
            )
        return self.get(idea_id) if cur.rowcount else None

    def delete(self, idea_id: int) -> bool:
        with self._conn() as conn:
            cur = conn.execute("DELETE FROM ideas WHERE id = ?", (idea_id,))
        return cur.rowcount > 0
