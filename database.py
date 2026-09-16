"""Gönderilen ilanların kalıcı olarak takip edilmesi."""

import sqlite3

from config import DATABASE_PATH


def _connection() -> sqlite3.Connection:
    return sqlite3.connect(DATABASE_PATH)


def initialize_database() -> None:
    with _connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS seen_jobs (
                job_id TEXT PRIMARY KEY,
                seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def is_seen(job_id: str) -> bool:
    with _connection() as connection:
        row = connection.execute(
            "SELECT 1 FROM seen_jobs WHERE job_id = ?", (job_id,)
        ).fetchone()
    return row is not None


def mark_as_seen(job_id: str) -> None:
    with _connection() as connection:
        connection.execute(
            "INSERT OR IGNORE INTO seen_jobs (job_id) VALUES (?)", (job_id,)
        )
