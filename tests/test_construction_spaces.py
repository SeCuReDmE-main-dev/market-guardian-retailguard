# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

from __future__ import annotations

import unittest

from src.construction import ArtifactStatus, BuilderLane, ConstructionArtifact, IntegrationDecision


class ConstructionSpaceTests(unittest.TestCase):
    def test_construction_artifact_validates_required_fields(self) -> None:
        with self.assertRaises(ValueError):
            ConstructionArtifact(
                artifact_id="",
                lane=BuilderLane.JEAN_SEBASTIEN,
                title="Visual primitive note",
                summary="Human-origin visual concept.",
            )
        with self.assertRaises(ValueError):
            ConstructionArtifact(
                artifact_id="js-1",
                lane=BuilderLane.JEAN_SEBASTIEN,
                title="",
                summary="Human-origin visual concept.",
            )

    def test_construction_artifact_is_metadata_only(self) -> None:
        with self.assertRaises(ValueError):
            ConstructionArtifact(
                artifact_id="codex-1",
                lane=BuilderLane.CODEX,
                title="Bad source",
                summary="Should reject raw visual media references.",
                source_refs=("camera/raw_frame_bytes/1",),
            )

    def test_construction_artifact_to_dict(self) -> None:
        artifact = ConstructionArtifact(
            artifact_id="js-vis-1",
            lane=BuilderLane.JEAN_SEBASTIEN,
            title="V.I.S Guardian naming",
            summary="Human-origin visual naming concept.",
            source_refs=("docs/vision/README.md",),
            status=ArtifactStatus.REVIEWED,
        )
        self.assertEqual(
            {
                "artifact_id": "js-vis-1",
                "lane": "jean_sebastien",
                "title": "V.I.S Guardian naming",
                "summary": "Human-origin visual naming concept.",
                "source_refs": ["docs/vision/README.md"],
                "status": "reviewed",
            },
            artifact.to_dict(),
        )

    def test_integration_decision_validates_required_fields(self) -> None:
        with self.assertRaises(ValueError):
            IntegrationDecision(
                decision_id="",
                human_artifact_id="js-1",
                codex_artifact_id="codex-1",
                accepted_output="V.I.S Guardian",
                rationale="Bounded visual module name.",
                timestamp_ms=1,
            )
        with self.assertRaises(ValueError):
            IntegrationDecision(
                decision_id="int-1",
                human_artifact_id="js-1",
                codex_artifact_id="codex-1",
                accepted_output="V.I.S Guardian",
                rationale="",
                timestamp_ms=1,
            )

    def test_construction_artifacts_do_not_bypass_safety_language(self) -> None:
        artifact = ConstructionArtifact(
            artifact_id="codex-review-1",
            lane=BuilderLane.CODEX,
            title="Review packet",
            summary="Use review required language for unresolved contradiction.",
            source_refs=("tests/test_governance.py",),
        )
        self.assertIn("review required", artifact.summary)
        self.assertNotIn("confirmed", artifact.summary.lower())


if __name__ == "__main__":
    unittest.main()
