# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Recalibration decisions from Neutro scores and tracking guardrails."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .scoring import NeutroAgentScore


class NeutroAction(str, Enum):
    CONTINUE = "continue"
    RECALIBRATE = "recalibrate"
    FREEZE = "freeze"
    SPLIT = "split"
    MERGE = "merge"
    QUARANTINE = "quarantine"
    HUMAN_REVIEW = "human_review"


@dataclass(frozen=True)
class NeutroDecision:
    action: NeutroAction
    reason: str

    def to_dict(self) -> dict[str, str]:
        return {"action": self.action.value, "reason": self.reason}


def decide_recalibration(
    score: NeutroAgentScore,
    *,
    track_purity: float = 1.0,
    unsupported_claims: int = 0,
) -> NeutroDecision:
    if not 0.0 <= track_purity <= 1.0:
        raise ValueError("track_purity must be in [0, 1]")
    if unsupported_claims < 0:
        raise ValueError("unsupported_claims must be >= 0")

    if unsupported_claims:
        return NeutroDecision(NeutroAction.QUARANTINE, "unsupported_claims")
    if track_purity < 0.65:
        return NeutroDecision(NeutroAction.FREEZE, "track_purity_drop")
    if score.max_dF >= 0.85 or score.value.F_system >= 0.75:
        return NeutroDecision(NeutroAction.HUMAN_REVIEW, "high_contradiction")
    if score.value.I_system >= 0.6 or score.complexity.D_f_hat >= 0.75:
        return NeutroDecision(NeutroAction.RECALIBRATE, "high_ambiguity")
    return NeutroDecision(NeutroAction.CONTINUE, "bounded_evidence")
