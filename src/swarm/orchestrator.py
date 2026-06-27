# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Store-level orchestrator for bounded customer agents."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.neutro import NeutroAgentScore, score_agent
from src.vision import (
    TrackContinuityScore,
    VisualPrimitive,
    VisualPrimitiveKind,
    visual_contradictions_to_divergence,
    visual_primitives_to_agent_evidence,
)

from .agents import BasketItemHypothesis, CustomerAgent


@dataclass
class StoreOrchestrator:
    agents: dict[str, CustomerAgent] = field(default_factory=dict)
    visual_primitives: dict[str, list[VisualPrimitive]] = field(default_factory=dict)

    def customer_entered(self, track_id: str, zone: str, timestamp_ms: int) -> CustomerAgent:
        if track_id in self.agents:
            return self.agents[track_id]
        agent = CustomerAgent(track_id=track_id, zone=zone, created_at_ms=timestamp_ms)
        self.agents[track_id] = agent
        return agent

    def update_track_purity(self, track_id: str, value: float) -> None:
        self._agent(track_id).update_track_purity(value)

    def add_basket_item(
        self,
        track_id: str,
        *,
        sku: str,
        label: str,
        evidence_id: str,
        confidence: float,
    ) -> None:
        item = BasketItemHypothesis(
            sku=sku,
            label=label,
            evidence_id=evidence_id,
            confidence=confidence,
        )
        self._agent(track_id).basket.add_item(item)

    def ingest_visual_primitives(
        self,
        track_id: str,
        primitives: list[VisualPrimitive],
        *,
        continuity: TrackContinuityScore | None = None,
    ) -> None:
        agent = self._agent(track_id)
        if continuity is not None:
            if continuity.track_id != track_id:
                raise ValueError("continuity track_id must match visual track_id")
            agent.update_track_purity(continuity.purity)
        primitive_ids = [primitive.primitive_id for primitive in primitives]
        agent.record_visual_primitives(primitive_ids)
        self.visual_primitives.setdefault(track_id, []).extend(primitives)

    def score_visual_state(self, track_id: str) -> NeutroAgentScore:
        self._agent(track_id)
        primitives = self.visual_primitives.get(track_id, [])
        evidence = visual_primitives_to_agent_evidence(primitives)
        divergences = visual_contradictions_to_divergence(primitives)
        graph_complexity = _visual_graph_complexity(primitives)
        return score_agent(evidence, divergences, graph_complexity=graph_complexity)

    def _agent(self, track_id: str) -> CustomerAgent:
        try:
            return self.agents[track_id]
        except KeyError as exc:
            raise KeyError(f"unknown track_id: {track_id}") from exc


def _visual_graph_complexity(primitives: list[VisualPrimitive]) -> float:
    base = len(primitives) / 10
    occlusion_pressure = 0.6 * sum(1 for item in primitives if item.kind is VisualPrimitiveKind.OCCLUSION)
    saliency_pressure = 0.15 * sum(1 for item in primitives if item.kind is VisualPrimitiveKind.SALIENCY)
    return min(1.0, base + occlusion_pressure + saliency_pressure)
