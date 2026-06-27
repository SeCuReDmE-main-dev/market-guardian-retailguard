# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Small synthetic checkout replay for the first scaffold."""

from __future__ import annotations

from dataclasses import dataclass

from src.evidence import EvidenceEvent, EvidenceLedger, EventKind
from src.neutro import AgentDivergence, AgentEvidence, EvidenceKind, score_agent, decide_recalibration
from src.swarm import CashCloseAgent, HumanReviewAgent, ReviewCase, StoreOrchestrator


@dataclass(frozen=True)
class ReplayResult:
    review_cases: tuple[ReviewCase, ...]
    ledger_verified: bool
    basket_items: int
    cash_requires_review: bool


def run_checkout_replay(*, missed_scan: bool = False, cash_mismatch: float = 0.0) -> ReplayResult:
    ledger = EvidenceLedger()
    orchestrator = StoreOrchestrator()
    review_agent = HumanReviewAgent()
    cash_agent = CashCloseAgent()

    orchestrator.customer_entered("track-1", "entry", 0)
    detection = EvidenceEvent("detection-apple-1", EventKind.DETECTION, 100, {"label": "apple", "zone": "aisle-1"})
    ledger.append(detection)
    orchestrator.add_basket_item(
        "track-1",
        sku="apple",
        label="apple",
        evidence_id=detection.event_id,
        confidence=0.9,
    )

    evidence = [AgentEvidence(EvidenceKind.OBSERVED, detection.event_id, 0.9)]
    divergences = []
    if not missed_scan:
        pos = EvidenceEvent("pos-apple-1", EventKind.POS, 300, {"sku": "apple", "price": 1.25})
        ledger.append(pos)
        evidence.append(AgentEvidence(EvidenceKind.OBSERVED, pos.event_id, 1.0))
    else:
        divergences.append(AgentDivergence("basket_pos_mismatch", 0.9))

    score = score_agent(evidence, divergences)
    decision = decide_recalibration(score)
    cases = []
    if decision.action.value in {"human_review", "quarantine", "freeze", "recalibrate"}:
        cases.append(
            review_agent.open_case(
                case_id="case-1",
                status="unresolved_contradiction",
                evidence_ids=[detection.event_id],
                summary="Basket and checkout evidence require operator review.",
            )
        )

    cash_result = cash_agent.reconcile(expected_cash=1000.0, counted_cash=1000.0 + cash_mismatch)
    if cash_result.requires_review:
        event = EvidenceEvent("cash-close-1", EventKind.CASH_CLOSE, 1000, {"mismatch": cash_result.mismatch})
        ledger.append(event)
        cases.append(
            review_agent.open_case(
                case_id="cash-case-1",
                status="review_required",
                evidence_ids=[event.event_id],
                summary="End-of-day cash close mismatch crossed the review threshold.",
            )
        )

    return ReplayResult(
        review_cases=tuple(cases),
        ledger_verified=ledger.verify(),
        basket_items=orchestrator.agents["track-1"].basket.item_count(),
        cash_requires_review=cash_result.requires_review,
    )
