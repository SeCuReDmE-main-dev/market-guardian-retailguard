# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Metadata-only evidence events."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import json
from typing import Any


class EventKind(str, Enum):
    DETECTION = "detection"
    POS = "pos"
    INVENTORY = "inventory"
    SYNTHETIC_REPLAY = "synthetic_replay"
    CASH_CLOSE = "cash_close"
    OPERATOR = "operator"


FORBIDDEN_METADATA_KEYS = {"raw_frame", "raw_frame_bytes", "image_bytes", "video_bytes"}


@dataclass(frozen=True)
class EvidenceEvent:
    event_id: str
    kind: EventKind
    timestamp_ms: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.event_id:
            raise ValueError("event_id is required")
        if self.timestamp_ms < 0:
            raise ValueError("timestamp_ms must be >= 0")
        forbidden = FORBIDDEN_METADATA_KEYS.intersection(self.metadata)
        if forbidden:
            raise ValueError(f"raw media metadata is not allowed by default: {sorted(forbidden)}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "kind": self.kind.value,
            "timestamp_ms": self.timestamp_ms,
            "metadata": self.metadata,
        }


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
