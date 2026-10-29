from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class QueueJob:
    id: str
    title: str
    state: str = "CREATED"
    created_at: str = ""
    attempts: int = 0
    max_attempts: int = 5
    metadata: Dict[str, Any] = field(default_factory=dict)


class QueueManager:
    def __init__(self, db) -> None:
        self.db = db

    def enqueue(self, job: QueueJob) -> QueueJob:
        self.db.add_job({
            "id": job.id,
            "title": job.title,
            "source_url": job.metadata.get("source_url"),
            "state": job.state,
            "attempts": job.attempts,
            "max_attempts": job.max_attempts,
            "channel_id": job.metadata.get("channel_id"),
            "artifact_path": job.metadata.get("artifact_path"),
            "output_path": job.metadata.get("output_path"),
            "error": job.metadata.get("error"),
            "metadata": job.metadata,
        })
        return job

    def list_pending(self) -> List[QueueJob]:
        rows = self.db.list_jobs()
        return [QueueJob(**{"id": row["id"], "title": row["title"], "state": row["state"], "created_at": "", "attempts": row["attempts"], "max_attempts": row["max_attempts"], "metadata": row["metadata"]}) for row in rows if row["state"] not in {"PUBLISHED", "CANCELLED"}]

    def claim(self, job_id: str) -> Optional[QueueJob]:
        job = self.db.get_job(job_id)
        if job is None:
            return None
        self.db.update_job(job_id, state="QUEUED", attempts=job["attempts"] + 1)
        return QueueJob(id=job["id"], title=job["title"], state="QUEUED", created_at="", attempts=job["attempts"] + 1, max_attempts=job["max_attempts"], metadata=job["metadata"])
