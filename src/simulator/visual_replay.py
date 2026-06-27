# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Synthetic V.I.S Guardian replay scenarios."""

from __future__ import annotations

from dataclasses import dataclass

from src.neutro import NeutroAction, decide_recalibration
from src.swarm import CustomerAgentStatus, StoreOrchestrator
from src.vision import TrackContinuityScore, VisualPrimitive, VisualPrimitiveKind


@dataclass(frozen=True)
class VisualReplayResult:
    action: NeutroAction
    agent_status: CustomerAgentStatus
    visual_primitive_count: int
    basket_items: int
    max_dF: float


def normal_visual_tracking() -> VisualReplayResult:
    return _run_visual_replay(
        [
            VisualPrimitive("vp-object-1", VisualPrimitiveKind.OBJECT_PRESENCE, "detection-item-1", 0.92, "aisle-1", 10),
            VisualPrimitive("vp-motion-1", VisualPrimitiveKind.MOTION, "motion-track-1", 0.86, "aisle-1", 20),
            VisualPrimitive("vp-contour-1", VisualPrimitiveKind.CONTOUR, "contour-item-1", 0.8, "aisle-1", 30),
        ]
    )


def temporary_occlusion() -> VisualReplayResult:
    return _run_visual_replay(
        [
            VisualPrimitive("vp-object-1", VisualPrimitiveKind.OBJECT_PRESENCE, "detection-item-1", 0.85, "aisle-1", 10),
            VisualPrimitive("vp-occlusion-1", VisualPrimitiveKind.OCCLUSION, "occlusion-shelf-1", 0.95, "aisle-1", 20),
        ]
    )


def track_split() -> VisualReplayResult:
    return _run_visual_replay(
        [
            VisualPrimitive("vp-track-1", VisualPrimitiveKind.TRACK_CONTINUITY, "track-continuity-1", 0.4, "entry", 10),
        ],
        continuity=TrackContinuityScore("track-1", purity=0.4, occlusion_pressure=0.6, handoff_risk=0.8),
    )


def ambiguous_hand_to_shelf_motion() -> VisualReplayResult:
    return _run_visual_replay(
        [
            VisualPrimitive("vp-motion-1", VisualPrimitiveKind.MOTION, "motion-hand-shelf-1", 0.58, "aisle-2", 10),
            VisualPrimitive("vp-saliency-1", VisualPrimitiveKind.SALIENCY, "saliency-shelf-1", 0.72, "aisle-2", 12),
            VisualPrimitive("vp-occlusion-1", VisualPrimitiveKind.OCCLUSION, "occlusion-hand-1", 0.8, "aisle-2", 15),
        ]
    )


def basket_pos_visual_mismatch() -> VisualReplayResult:
    return _run_visual_replay(
        [
            VisualPrimitive("vp-object-1", VisualPrimitiveKind.OBJECT_PRESENCE, "detection-item-1", 0.9, "checkout", 10),
            VisualPrimitive(
                "vp-contradiction-1",
                VisualPrimitiveKind.SCENE_CONTRADICTION,
                "visual-pos-mismatch-1",
                0.95,
                "checkout",
                20,
            ),
        ]
    )


def _run_visual_replay(
    primitives: list[VisualPrimitive],
    *,
    continuity: TrackContinuityScore | None = None,
) -> VisualReplayResult:
    orchestrator = StoreOrchestrator()
    agent = orchestrator.customer_entered("track-1", "entry", 0)
    orchestrator.ingest_visual_primitives(agent.track_id, primitives, continuity=continuity)
    score = orchestrator.score_visual_state(agent.track_id)
    decision = decide_recalibration(score, track_purity=agent.track_purity)
    return VisualReplayResult(
        action=decision.action,
        agent_status=agent.status,
        visual_primitive_count=len(agent.visual_primitive_ids),
        basket_items=agent.basket.item_count(),
        max_dF=score.max_dF,
    )
