"""Database utilities for the notes backend.

This backend uses SQLite. In this Kavia multi-container setup, the SQLite database
lives in a separate `database` container and exposes the database file path via
the SQLITE_DB environment variable.

If SQLITE_DB is not set (e.g., local development), we fall back to a local file
in the backend container directory so the app can still run.
"""

from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Iterator


def _utc_now_iso() -> str:
    """Return current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get_db_path() -> str:
    """Return the SQLite DB file path.

    Environment:
        SQLITE_DB: Absolute path to the SQLite database file (provided by database container).

    Returns:
        str: Path to the sqlite database file.
    """
    env_path = os.getenv("SQLITE_DB")
    if env_path:
        return env_path

    # Fallback for local/dev (no separate DB container wired in)
    return os.path.join(os.getcwd(), "notes.db")


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Context manager yielding an SQLite connection with safe defaults."""
    db_path = get_db_path()

    # check_same_thread=False allows usage from FastAPI threadpool workers.
    conn = sqlite3.connect(db_path, check_same_thread=False)
    try:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Initialize DB schema if it doesn't exist."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def ensure_db_ready() -> None:
    """Ensure the database is ready to serve requests."""
    init_db()


def utc_now_iso() -> str:
    """Public helper for consistent timestamp formatting."""
    return _utc_now_iso()
