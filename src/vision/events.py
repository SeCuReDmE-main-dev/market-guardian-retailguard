# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Visual integrity events built from metadata-only primitives."""

from __future__ import annotations

from dataclasses import dataclass


TEMPORARY_TRACK_PREFIXES = ("track-", "temp-track-")


@dataclass(frozen=True)
class VisualIntegrityEvent:
    event_id: str
    track_id: str
    primitive_ids: tuple[str, ...]
    summary: str
    ambiguity_score: float

    def __post_init__(self) -> None:
        if not self.event_id:
            raise ValueError("event_id is required")
        if not self.track_id:
            raise ValueError("track_id is required")
        if not self.track_id.startswith(TEMPORARY_TRACK_PREFIXES):
            raise ValueError("track_id must be a temporary anonymous track reference")
        if not self.primitive_ids:
            raise ValueError("at least one primitive_id is required")
        if not self.summary:
            raise ValueError("summary is required")
        if not 0.0 <= self.ambiguity_score <= 1.0:
            raise ValueError("ambiguity_score must be in [0, 1]")
        object.__setattr__(self, "primitive_ids", tuple(self.primitive_ids))

    def to_dict(self) -> dict[str, object]:
        return {
            "event_id": self.event_id,
            "track_id": self.track_id,
            "primitive_ids": list(self.primitive_ids),
            "summary": self.summary,
            "ambiguity_score": self.ambiguity_score,
        }
