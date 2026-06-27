# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Store-level orchestrator for bounded customer agents."""

from __future__ import annotations

from dataclasses import dataclass, field

from .agents import BasketItemHypothesis, CustomerAgent


@dataclass
class StoreOrchestrator:
    agents: dict[str, CustomerAgent] = field(default_factory=dict)

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

    def _agent(self, track_id: str) -> CustomerAgent:
        try:
            return self.agents[track_id]
        except KeyError as exc:
            raise KeyError(f"unknown track_id: {track_id}") from exc
