# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

from __future__ import annotations

import unittest

from src.neutro import EvidenceKind, NeutroAction, decide_recalibration, score_agent
from src.vision import (
    VisualPrimitive,
    VisualPrimitiveKind,
    visual_contradictions_to_divergence,
    visual_primitives_to_agent_evidence,
)


class VisionBridgeTests(unittest.TestCase):
    def test_visual_primitives_become_evidence_not_basket_facts(self) -> None:
        primitives = [
            VisualPrimitive("vp-object-1", VisualPrimitiveKind.OBJECT_PRESENCE, "detection-1", 0.9, "aisle", 1),
            VisualPrimitive("vp-saliency-1", VisualPrimitiveKind.SALIENCY, "saliency-1", 0.7, "aisle", 2),
        ]
        evidence = visual_primitives_to_agent_evidence(primitives)
        self.assertEqual([EvidenceKind.OBSERVED, EvidenceKind.INFERRED], [item.kind for item in evidence])
        self.assertEqual(["detection-1", "saliency-1"], [item.event_id for item in evidence])
        self.assertFalse(any(hasattr(item, "sku") for item in evidence))

    def test_occlusion_increases_indeterminacy(self) -> None:
        primitives = [
            VisualPrimitive("vp-object-1", VisualPrimitiveKind.OBJECT_PRESENCE, "detection-1", 0.9, "aisle", 1),
            VisualPrimitive("vp-occlusion-1", VisualPrimitiveKind.OCCLUSION, "occlusion-1", 0.9, "aisle", 2),
        ]
        evidence = visual_primitives_to_agent_evidence(primitives)
        score = score_agent(evidence)
        self.assertIn(EvidenceKind.UNKNOWN, [item.kind for item in evidence])
        self.assertGreater(score.value.I_system, 0.0)

    def test_scene_contradiction_can_trigger_human_review(self) -> None:
        primitives = [
            VisualPrimitive("vp-object-1", VisualPrimitiveKind.OBJECT_PRESENCE, "detection-1", 0.9, "checkout", 1),
            VisualPrimitive(
                "vp-contradiction-1",
                VisualPrimitiveKind.SCENE_CONTRADICTION,
                "visual-pos-mismatch-1",
                0.95,
                "checkout",
                2,
            ),
        ]
        evidence = visual_primitives_to_agent_evidence(primitives)
        divergences = visual_contradictions_to_divergence(primitives)
        decision = decide_recalibration(score_agent(evidence, divergences))
        self.assertEqual(NeutroAction.HUMAN_REVIEW, decision.action)


if __name__ == "__main__":
    unittest.main()
