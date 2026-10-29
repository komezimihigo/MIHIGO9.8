from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


class Database:
    def __init__(self, db_path: str = "data/mihigo.sqlite3") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._connect()
        self._init_schema()

    def _connect(self) -> None:
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def _init_schema(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                source_url TEXT,
                state TEXT NOT NULL,
                attempts INTEGER DEFAULT 0,
                max_attempts INTEGER DEFAULT 5,
                channel_id TEXT,
                artifact_path TEXT,
                output_path TEXT,
                error TEXT,
                metadata TEXT DEFAULT '{}'
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS job_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT NOT NULL,
                state TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                metadata TEXT DEFAULT '{}'
            )
            """
        )
        self.conn.commit()

    def add_job(self, job: Dict[str, Any]) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO jobs (id, title, source_url, state, attempts, max_attempts, channel_id, artifact_path, output_path, error, metadata) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                job["id"],
                job["title"],
                job.get("source_url"),
                job.get("state", "CREATED"),
                job.get("attempts", 0),
                job.get("max_attempts", 5),
                job.get("channel_id"),
                job.get("artifact_path"),
                job.get("output_path"),
                job.get("error"),
                json.dumps(job.get("metadata", {})),
            ),
        )
        self.conn.commit()

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        row = self.conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        if row is None:
            return None
        return {
            "id": row["id"],
            "title": row["title"],
            "source_url": row["source_url"],
            "state": row["state"],
            "attempts": row["attempts"],
            "max_attempts": row["max_attempts"],
            "channel_id": row["channel_id"],
            "artifact_path": row["artifact_path"],
            "output_path": row["output_path"],
            "error": row["error"],
            "metadata": json.loads(row["metadata"] or "{}"),
        }

    def update_job(self, job_id: str, **kwargs: Any) -> None:
        fields = []
        values = []
        for key, value in kwargs.items():
            if key == "metadata":
                value = json.dumps(value)
            fields.append(f"{key} = ?")
            values.append(value)
        values.append(job_id)
        self.conn.execute(f"UPDATE jobs SET {', '.join(fields)} WHERE id = ?", tuple(values))
        self.conn.commit()

    def list_jobs(self, state: Optional[str] = None) -> List[Dict[str, Any]]:
        if state:
            rows = self.conn.execute("SELECT * FROM jobs WHERE state = ? ORDER BY id", (state,)).fetchall()
        else:
            rows = self.conn.execute("SELECT * FROM jobs ORDER BY id").fetchall()
        return [self.get_job(row["id"]) for row in rows]
