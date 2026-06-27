# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

from __future__ import annotations

import unittest

from src.vision import TrackContinuityScore, VisualIntegrityEvent, VisualPrimitive, VisualPrimitiveKind


class VisionCoreTests(unittest.TestCase):
    def test_visual_primitive_validates_required_fields(self) -> None:
        with self.assertRaises(ValueError):
            VisualPrimitive("", VisualPrimitiveKind.CONTOUR, "evidence-1", 0.8, "aisle", 1)
        with self.assertRaises(ValueError):
            VisualPrimitive("vp-1", VisualPrimitiveKind.CONTOUR, "", 0.8, "aisle", 1)
        with self.assertRaises(ValueError):
            VisualPrimitive("vp-1", VisualPrimitiveKind.CONTOUR, "evidence-1", 1.2, "aisle", 1)
        with self.assertRaises(ValueError):
            VisualPrimitive("vp-1", VisualPrimitiveKind.CONTOUR, "evidence-1", 0.8, "aisle", -1)

    def test_visual_primitive_rejects_raw_media_references(self) -> None:
        with self.assertRaises(ValueError):
            VisualPrimitive("vp-raw-frame-1", VisualPrimitiveKind.CONTOUR, "evidence-1", 0.8, "aisle", 1)
        with self.assertRaises(ValueError):
            VisualPrimitive("vp-1", VisualPrimitiveKind.CONTOUR, "camera-image_bytes-1", 0.8, "aisle", 1)

    def test_visual_integrity_event_validates_temporary_track(self) -> None:
        event = VisualIntegrityEvent(
            event_id="vis-event-1",
            track_id="track-1",
            primitive_ids=("vp-1",),
            summary="Visual ambiguity requires review.",
            ambiguity_score=0.7,
        )
        self.assertEqual("track-1", event.to_dict()["track_id"])
        with self.assertRaises(ValueError):
            VisualIntegrityEvent("vis-event-2", "person-1", ("vp-1",), "Invalid identity track.", 0.2)
        with self.assertRaises(ValueError):
            VisualIntegrityEvent("vis-event-3", "track-1", tuple(), "Missing primitive refs.", 0.2)
        with self.assertRaises(ValueError):
            VisualIntegrityEvent("vis-event-4", "track-1", ("vp-1",), "Bad ambiguity.", 1.2)

    def test_track_continuity_freeze_threshold(self) -> None:
        stable = TrackContinuityScore("track-1", purity=0.8, occlusion_pressure=0.2, handoff_risk=0.1)
        split = TrackContinuityScore("track-1", purity=0.4, occlusion_pressure=0.8, handoff_risk=0.9)
        self.assertFalse(stable.requires_freeze())
        self.assertTrue(split.requires_freeze())


if __name__ == "__main__":
    unittest.main()
