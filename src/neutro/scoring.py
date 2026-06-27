# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Evidence-bound Neutro scoring for customer agents."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .value import FractalComplexity, LocalTension, NeutroValue


class EvidenceKind(str, Enum):
    OBSERVED = "observed"
    INFERRED = "inferred"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class AgentEvidence:
    """Evidence item tied to an event identifier."""

    kind: EvidenceKind
    event_id: str
    confidence: float = 1.0

    def __post_init__(self) -> None:
        if not self.event_id:
            raise ValueError("event_id is required")
        if not 0.0 <= float(self.confidence) <= 1.0:
            raise ValueError("confidence must be in [0, 1]")


@dataclass(frozen=True)
class AgentDivergence:
    """A structured disagreement between evidence channels."""

    relation: str
    severity: float

    def __post_init__(self) -> None:
        if not self.relation:
            raise ValueError("relation is required")
        if not 0.0 <= float(self.severity) <= 1.0:
            raise ValueError("severity must be in [0, 1]")


@dataclass(frozen=True)
class NeutroAgentScore:
    value: NeutroValue
    local_tensions: tuple[LocalTension, ...]
    complexity: FractalComplexity

    @property
    def max_dF(self) -> float:
        if not self.local_tensions:
            return 0.0
        return max(tension.dF for tension in self.local_tensions)

    def to_dict(self) -> dict[str, object]:
        return {
            "value": self.value.to_dict(),
            "local_tensions": [tension.to_dict() for tension in self.local_tensions],
            "complexity": self.complexity.to_dict(),
            "max_dF": self.max_dF,
        }


def score_agent(
    evidence: list[AgentEvidence],
    divergences: list[AgentDivergence] | None = None,
    *,
    graph_complexity: float = 0.0,
) -> NeutroAgentScore:
    """Score one agent from explicit evidence and divergences."""

    divergences = divergences or []
    if not evidence:
        return NeutroAgentScore(
            value=NeutroValue(0.0, 1.0, 0.0),
            local_tensions=tuple(LocalTension(item.relation, item.severity) for item in divergences),
            complexity=FractalComplexity(graph_complexity),
        )

    observed = [item.confidence for item in evidence if item.kind is EvidenceKind.OBSERVED]
    inferred = [item.confidence for item in evidence if item.kind is EvidenceKind.INFERRED]
    unknown = [item.confidence for item in evidence if item.kind is EvidenceKind.UNKNOWN]

    total_weight = len(evidence) + len(divergences)
    observed_support = sum(observed) / total_weight
    inferred_support = 0.5 * sum(inferred) / total_weight
    unknown_pressure = sum(max(0.25, value) for value in unknown) / total_weight
    divergence_pressure = sum(item.severity for item in divergences) / max(1, total_weight)

    T_system = min(1.0, observed_support + inferred_support)
    I_system = min(1.0, unknown_pressure + (0.5 * divergence_pressure))
    F_system = min(1.0, divergence_pressure)

    return NeutroAgentScore(
        value=NeutroValue(T_system, I_system, F_system),
        local_tensions=tuple(LocalTension(item.relation, item.severity) for item in divergences),
        complexity=FractalComplexity(graph_complexity),
    )
