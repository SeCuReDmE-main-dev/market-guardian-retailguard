# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Bounded agents for one-customer-at-a-time tracking."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CustomerAgentStatus(str, Enum):
    ACTIVE = "active"
    FROZEN = "frozen"
    EXITED = "exited"


@dataclass(frozen=True)
class BasketItemHypothesis:
    sku: str
    label: str
    evidence_id: str
    confidence: float

    def __post_init__(self) -> None:
        if not self.sku:
            raise ValueError("sku is required")
        if not self.label:
            raise ValueError("label is required")
        if not self.evidence_id:
            raise ValueError("evidence_id is required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0, 1]")


@dataclass
class BasketHypothesisAgent:
    track_id: str
    items: list[BasketItemHypothesis] = field(default_factory=list)

    def add_item(self, item: BasketItemHypothesis) -> None:
        self.items.append(item)

    def item_count(self) -> int:
        return len(self.items)


@dataclass
class CustomerAgent:
    track_id: str
    zone: str
    created_at_ms: int
    ttl_ms: int = 30 * 60 * 1000
    status: CustomerAgentStatus = CustomerAgentStatus.ACTIVE
    track_purity: float = 1.0
    visual_primitive_ids: list[str] = field(default_factory=list)
    basket: BasketHypothesisAgent = field(init=False)

    def __post_init__(self) -> None:
        if not self.track_id:
            raise ValueError("track_id is required")
        if not self.zone:
            raise ValueError("zone is required")
        if self.created_at_ms < 0:
            raise ValueError("created_at_ms must be >= 0")
        if self.ttl_ms <= 0:
            raise ValueError("ttl_ms must be > 0")
        if not 0.0 <= self.track_purity <= 1.0:
            raise ValueError("track_purity must be in [0, 1]")
        self.basket = BasketHypothesisAgent(self.track_id)

    def update_track_purity(self, value: float) -> None:
        if not 0.0 <= value <= 1.0:
            raise ValueError("track_purity must be in [0, 1]")
        self.track_purity = value
        if value < 0.65:
            self.status = CustomerAgentStatus.FROZEN

    def expire_if_needed(self, now_ms: int) -> None:
        if now_ms - self.created_at_ms > self.ttl_ms:
            self.status = CustomerAgentStatus.EXITED

    def record_visual_primitives(self, primitive_ids: list[str]) -> None:
        for primitive_id in primitive_ids:
            if not primitive_id:
                raise ValueError("primitive_id is required")
        self.visual_primitive_ids.extend(primitive_ids)
