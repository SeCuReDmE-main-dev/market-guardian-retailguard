# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Metadata-only visual primitives for V.I.S Guardian."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


FORBIDDEN_VISUAL_REF_PARTS = {
    "raw_frame",
    "raw-frame",
    "raw_frame_bytes",
    "raw-frame-bytes",
    "image_bytes",
    "image-bytes",
    "video_bytes",
    "video-bytes",
    "faceprint",
    "biometric",
}


class VisualPrimitiveKind(str, Enum):
    CONTOUR = "contour"
    MOTION = "motion"
    SALIENCY = "saliency"
    OCCLUSION = "occlusion"
    TRACK_CONTINUITY = "track_continuity"
    OBJECT_PRESENCE = "object_presence"
    SCENE_CONTRADICTION = "scene_contradiction"


@dataclass(frozen=True)
class VisualPrimitive:
    primitive_id: str
    kind: VisualPrimitiveKind
    evidence_id: str
    confidence: float
    zone: str
    timestamp_ms: int

    def __post_init__(self) -> None:
        if not self.primitive_id:
            raise ValueError("primitive_id is required")
        if not self.evidence_id:
            raise ValueError("evidence_id is required")
        if not self.zone:
            raise ValueError("zone is required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0, 1]")
        if self.timestamp_ms < 0:
            raise ValueError("timestamp_ms must be >= 0")
        _validate_metadata_ref(self.primitive_id, "primitive_id")
        _validate_metadata_ref(self.evidence_id, "evidence_id")

    def to_dict(self) -> dict[str, object]:
        return {
            "primitive_id": self.primitive_id,
            "kind": self.kind.value,
            "evidence_id": self.evidence_id,
            "confidence": self.confidence,
            "zone": self.zone,
            "timestamp_ms": self.timestamp_ms,
        }


def _validate_metadata_ref(value: str, field_name: str) -> None:
    normalized = value.lower()
    forbidden = [part for part in FORBIDDEN_VISUAL_REF_PARTS if part in normalized]
    if forbidden:
        raise ValueError(f"{field_name} must be metadata-only: {sorted(forbidden)}")
