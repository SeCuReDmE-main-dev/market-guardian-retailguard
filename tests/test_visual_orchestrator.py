# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

from __future__ import annotations

import unittest

from src.neutro import NeutroAction, decide_recalibration
from src.swarm import CustomerAgentStatus, StoreOrchestrator
from src.vision import TrackContinuityScore, VisualPrimitive, VisualPrimitiveKind


class VisualOrchestratorTests(unittest.TestCase):
    def test_unknown_track_rejects_visual_ingestion(self) -> None:
        orchestrator = StoreOrchestrator()
        primitive = VisualPrimitive("vp-1", VisualPrimitiveKind.CONTOUR, "contour-1", 0.8, "aisle", 1)
        with self.assertRaises(KeyError):
            orchestrator.ingest_visual_primitives("track-missing", [primitive])

    def test_visual_ingestion_stores_primitive_ids_only(self) -> None:
        orchestrator = StoreOrchestrator()
        agent = orchestrator.customer_entered("track-1", "entry", 0)
        primitive = VisualPrimitive("vp-1", VisualPrimitiveKind.OBJECT_PRESENCE, "detection-1", 0.9, "aisle", 1)
        orchestrator.ingest_visual_primitives(agent.track_id, [primitive])
        self.assertEqual(["vp-1"], agent.visual_primitive_ids)
        self.assertEqual(0, agent.basket.item_count())

    def test_raw_visual_media_is_rejected_before_ingestion(self) -> None:
        with self.assertRaises(ValueError):
            VisualPrimitive("vp-1", VisualPrimitiveKind.MOTION, "raw_frame-1", 0.9, "aisle", 1)

    def test_visual_ambiguity_can_recalibrate(self) -> None:
        orchestrator = StoreOrchestrator()
        agent = orchestrator.customer_entered("track-1", "entry", 0)
        primitives = [
            VisualPrimitive("vp-occlusion-1", VisualPrimitiveKind.OCCLUSION, "occlusion-1", 0.9, "aisle", 1),
            VisualPrimitive("vp-occlusion-2", VisualPrimitiveKind.OCCLUSION, "occlusion-2", 0.8, "aisle", 2),
        ]
        orchestrator.ingest_visual_primitives(agent.track_id, primitives)
        decision = decide_recalibration(orchestrator.score_visual_state(agent.track_id))
        self.assertEqual(NeutroAction.RECALIBRATE, decision.action)

    def test_cross_person_contamination_freezes_agent(self) -> None:
        orchestrator = StoreOrchestrator()
        agent = orchestrator.customer_entered("track-1", "entry", 0)
        primitive = VisualPrimitive("vp-track-1", VisualPrimitiveKind.TRACK_CONTINUITY, "track-continuity-1", 0.4, "entry", 1)
        continuity = TrackContinuityScore("track-1", purity=0.4, occlusion_pressure=0.7, handoff_risk=0.9)
        orchestrator.ingest_visual_primitives(agent.track_id, [primitive], continuity=continuity)
        self.assertEqual(CustomerAgentStatus.FROZEN, agent.status)


if __name__ == "__main__":
    unittest.main()
