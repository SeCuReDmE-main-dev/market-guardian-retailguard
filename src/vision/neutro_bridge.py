# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Bridge V.I.S Guardian primitives into Neutro evidence."""

from __future__ import annotations

from src.neutro import AgentDivergence, AgentEvidence, EvidenceKind

from .primitives import VisualPrimitive, VisualPrimitiveKind


OBSERVED_KINDS = {
    VisualPrimitiveKind.OBJECT_PRESENCE,
    VisualPrimitiveKind.MOTION,
    VisualPrimitiveKind.CONTOUR,
}
INFERRED_KINDS = {
    VisualPrimitiveKind.SALIENCY,
    VisualPrimitiveKind.TRACK_CONTINUITY,
}


def visual_primitives_to_agent_evidence(primitives: list[VisualPrimitive]) -> list[AgentEvidence]:
    evidence: list[AgentEvidence] = []
    for primitive in primitives:
        if primitive.kind is VisualPrimitiveKind.SCENE_CONTRADICTION:
            continue
        if primitive.kind in OBSERVED_KINDS and primitive.confidence >= 0.75:
            evidence.append(AgentEvidence(EvidenceKind.OBSERVED, primitive.evidence_id, primitive.confidence))
        elif primitive.kind in INFERRED_KINDS or primitive.kind in OBSERVED_KINDS:
            evidence.append(AgentEvidence(EvidenceKind.INFERRED, primitive.evidence_id, primitive.confidence))
        elif primitive.kind is VisualPrimitiveKind.OCCLUSION:
            evidence.append(AgentEvidence(EvidenceKind.UNKNOWN, primitive.evidence_id, primitive.confidence))
    return evidence


def visual_contradictions_to_divergence(primitives: list[VisualPrimitive]) -> list[AgentDivergence]:
    divergences: list[AgentDivergence] = []
    for primitive in primitives:
        if primitive.kind is VisualPrimitiveKind.SCENE_CONTRADICTION:
            divergences.append(AgentDivergence("visual_scene_contradiction", primitive.confidence))
    return divergences
