# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

import unittest

from src.neutro import (
    AgentDivergence,
    AgentEvidence,
    EvidenceKind,
    NeutroAction,
    NeutroValue,
    decide_recalibration,
    score_agent,
)


class NeutroScoringTests(unittest.TestCase):
    def test_neutro_value_bounds(self):
        value = NeutroValue(0.7, 0.2, 0.4)
        self.assertEqual(0.4, value.contradiction)
        with self.assertRaises(ValueError):
            NeutroValue(1.1, 0.0, 0.0)

    def test_unknown_evidence_increases_indeterminacy(self):
        score = score_agent([AgentEvidence(EvidenceKind.UNKNOWN, "event-1", 0.8)])
        self.assertGreater(score.value.I_system, score.value.T_system)

    def test_divergence_creates_local_tension(self):
        score = score_agent(
            [AgentEvidence(EvidenceKind.OBSERVED, "detection-1", 0.9)],
            [AgentDivergence("basket_pos_mismatch", 0.9)],
        )
        self.assertEqual(0.9, score.max_dF)
        decision = decide_recalibration(score)
        self.assertEqual(NeutroAction.HUMAN_REVIEW, decision.action)

    def test_unsupported_claims_are_quarantined(self):
        score = score_agent([AgentEvidence(EvidenceKind.OBSERVED, "detection-1", 0.9)])
        decision = decide_recalibration(score, unsupported_claims=1)
        self.assertEqual(NeutroAction.QUARANTINE, decision.action)


if __name__ == "__main__":
    unittest.main()
