# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Integration records for dual construction-space artifacts."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IntegrationDecision:
    decision_id: str
    human_artifact_id: str
    codex_artifact_id: str
    accepted_output: str
    rationale: str
    timestamp_ms: int

    def __post_init__(self) -> None:
        if not self.decision_id:
            raise ValueError("decision_id is required")
        if not self.human_artifact_id:
            raise ValueError("human_artifact_id is required")
        if not self.codex_artifact_id:
            raise ValueError("codex_artifact_id is required")
        if not self.accepted_output:
            raise ValueError("accepted_output is required")
        if not self.rationale:
            raise ValueError("rationale is required")
        if self.timestamp_ms < 0:
            raise ValueError("timestamp_ms must be >= 0")

    def to_dict(self) -> dict[str, object]:
        return {
            "decision_id": self.decision_id,
            "human_artifact_id": self.human_artifact_id,
            "codex_artifact_id": self.codex_artifact_id,
            "accepted_output": self.accepted_output,
            "rationale": self.rationale,
            "timestamp_ms": self.timestamp_ms,
        }
