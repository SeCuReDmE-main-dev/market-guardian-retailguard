# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Track continuity scoring for V.I.S Guardian."""

from __future__ import annotations

from dataclasses import dataclass


TRACK_PURITY_FREEZE_THRESHOLD = 0.65


@dataclass(frozen=True)
class TrackContinuityScore:
    track_id: str
    purity: float
    occlusion_pressure: float
    handoff_risk: float

    def __post_init__(self) -> None:
        if not self.track_id:
            raise ValueError("track_id is required")
        for field_name, value in {
            "purity": self.purity,
            "occlusion_pressure": self.occlusion_pressure,
            "handoff_risk": self.handoff_risk,
        }.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{field_name} must be in [0, 1]")

    def requires_freeze(self) -> bool:
        return self.purity < TRACK_PURITY_FREEZE_THRESHOLD

    def to_dict(self) -> dict[str, object]:
        return {
            "track_id": self.track_id,
            "purity": self.purity,
            "occlusion_pressure": self.occlusion_pressure,
            "handoff_risk": self.handoff_risk,
            "requires_freeze": self.requires_freeze(),
        }
