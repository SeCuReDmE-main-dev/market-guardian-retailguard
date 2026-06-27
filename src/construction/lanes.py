# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Construction lanes for human-origin and Codex-origin artifacts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


FORBIDDEN_SOURCE_REF_PARTS = {
    "raw_frame",
    "raw_frame_bytes",
    "image_bytes",
    "video_bytes",
    "biometric",
    "faceprint",
    "password",
    "secret",
    "api_key",
}


class BuilderLane(str, Enum):
    JEAN_SEBASTIEN = "jean_sebastien"
    CODEX = "codex"
    INTEGRATION = "integration"


class ArtifactStatus(str, Enum):
    DRAFT = "draft"
    REVIEWED = "reviewed"
    INTEGRATED = "integrated"
    REJECTED = "rejected"


@dataclass(frozen=True)
class ConstructionArtifact:
    artifact_id: str
    lane: BuilderLane
    title: str
    summary: str
    source_refs: tuple[str, ...] = field(default_factory=tuple)
    status: ArtifactStatus = ArtifactStatus.DRAFT

    def __post_init__(self) -> None:
        if not self.artifact_id:
            raise ValueError("artifact_id is required")
        if not self.title:
            raise ValueError("title is required")
        if not self.summary:
            raise ValueError("summary is required")
        refs = tuple(self.source_refs)
        object.__setattr__(self, "source_refs", refs)
        for source_ref in refs:
            _validate_source_ref(source_ref)

    def to_dict(self) -> dict[str, object]:
        return {
            "artifact_id": self.artifact_id,
            "lane": self.lane.value,
            "title": self.title,
            "summary": self.summary,
            "source_refs": list(self.source_refs),
            "status": self.status.value,
        }


def _validate_source_ref(source_ref: str) -> None:
    if not source_ref:
        raise ValueError("source_ref cannot be empty")
    normalized = source_ref.lower()
    forbidden = [part for part in FORBIDDEN_SOURCE_REF_PARTS if part in normalized]
    if forbidden:
        raise ValueError(f"source_ref must be metadata-only: {sorted(forbidden)}")
