from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional, List


class JobState(str, Enum):
    CREATED = "CREATED"
    WAITING_FOR_SOURCE = "WAITING_FOR_SOURCE"
    DISCOVERING = "DISCOVERING"
    SOURCE_VALIDATION = "SOURCE_VALIDATION"
    RIGHTS_REVIEW = "RIGHTS_REVIEW"
    QUEUED = "QUEUED"
    DOWNLOADING = "DOWNLOADING"
    ANALYZING = "ANALYZING"
    GENERATING_METADATA = "GENERATING_METADATA"
    RENDERING = "RENDERING"
    QUALITY_CHECK = "QUALITY_CHECK"
    READY_TO_PUBLISH = "READY_TO_PUBLISH"
    PUBLISHING = "PUBLISHING"
    PUBLISHED = "PUBLISHED"
    RETRY_WAIT = "RETRY_WAIT"
    FAILED = "FAILED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


VALID_TRANSITIONS = {
    JobState.CREATED: {JobState.WAITING_FOR_SOURCE, JobState.REJECTED, JobState.CANCELLED},
    JobState.WAITING_FOR_SOURCE: {JobState.DISCOVERING, JobState.REJECTED, JobState.CANCELLED},
    JobState.DISCOVERING: {JobState.SOURCE_VALIDATION, JobState.REJECTED, JobState.CANCELLED},
    JobState.SOURCE_VALIDATION: {JobState.RIGHTS_REVIEW, JobState.REJECTED, JobState.CANCELLED},
    JobState.RIGHTS_REVIEW: {JobState.QUEUED, JobState.REJECTED, JobState.CANCELLED},
    JobState.QUEUED: {JobState.DOWNLOADING, JobState.RETRY_WAIT, JobState.CANCELLED},
    JobState.DOWNLOADING: {JobState.ANALYZING, JobState.RETRY_WAIT, JobState.FAILED, JobState.CANCELLED},
    JobState.ANALYZING: {JobState.GENERATING_METADATA, JobState.RETRY_WAIT, JobState.FAILED, JobState.CANCELLED},
    JobState.GENERATING_METADATA: {JobState.RENDERING, JobState.RETRY_WAIT, JobState.FAILED, JobState.CANCELLED},
    JobState.RENDERING: {JobState.QUALITY_CHECK, JobState.RETRY_WAIT, JobState.FAILED, JobState.CANCELLED},
    JobState.QUALITY_CHECK: {JobState.READY_TO_PUBLISH, JobState.RETRY_WAIT, JobState.FAILED, JobState.CANCELLED},
    JobState.READY_TO_PUBLISH: {JobState.PUBLISHING, JobState.RETRY_WAIT, JobState.FAILED, JobState.CANCELLED},
    JobState.PUBLISHING: {JobState.PUBLISHED, JobState.RETRY_WAIT, JobState.FAILED, JobState.CANCELLED},
    JobState.PUBLISHED: {JobState.PUBLISHED},
    JobState.RETRY_WAIT: {JobState.QUEUED, JobState.CANCELLED},
    JobState.FAILED: {JobState.RETRY_WAIT, JobState.CANCELLED},
    JobState.REJECTED: {JobState.REJECTED},
    JobState.CANCELLED: {JobState.CANCELLED},
}


@dataclass
class ChannelConfig:
    id: str
    name: str
    enabled: bool = True
    daily_quota: int = 5
    preferred_output_format: str = "shorts"
    default_privacy: str = "private"
    timezone: str = "UTC"
    language: str = "en"


@dataclass
class SourceRecord:
    id: str
    source_url: str
    title: str
    creator: Optional[str] = None
    license_name: Optional[str] = None
    license_url: Optional[str] = None
    attribution: Optional[str] = None
    commercial_use: bool = False
    derivative_works: bool = False
    download_allowed: bool = False
    provenance_notes: str = ""
    approved: bool = False
    reason: str = ""
    canonical_hash: Optional[str] = None


@dataclass
class Job:
    id: str
    title: str
    source_url: Optional[str] = None
    state: JobState = JobState.CREATED
    attempts: int = 0
    max_attempts: int = 5
    channel_id: Optional[str] = None
    artifact_path: Optional[str] = None
    output_path: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    source: Optional[SourceRecord] = None
    created_at: str = ""
    updated_at: str = ""


class StateMachine:
    @staticmethod
    def can_transition(current: JobState, target: JobState) -> bool:
        return target in VALID_TRANSITIONS.get(current, set())

    @staticmethod
    def transition(job: Job, target: JobState, *, error: Optional[str] = None) -> None:
        if not StateMachine.can_transition(job.state, target):
            raise ValueError(f"Invalid state transition: {job.state.value} -> {target.value}")
        job.state = target
        job.error = error
        job.updated_at = "now"
