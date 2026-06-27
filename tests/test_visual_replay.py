# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

from __future__ import annotations

import unittest

from src.neutro import NeutroAction
from src.swarm import CustomerAgentStatus
from src.simulator import (
    ambiguous_hand_to_shelf_motion,
    basket_pos_visual_mismatch,
    normal_visual_tracking,
    temporary_occlusion,
    track_split,
)


class VisualReplayTests(unittest.TestCase):
    def test_normal_visual_tracking_continues(self) -> None:
        result = normal_visual_tracking()
        self.assertEqual(NeutroAction.CONTINUE, result.action)
        self.assertEqual(CustomerAgentStatus.ACTIVE, result.agent_status)
        self.assertEqual(0, result.basket_items)

    def test_temporary_occlusion_recalibrates(self) -> None:
        result = temporary_occlusion()
        self.assertEqual(NeutroAction.RECALIBRATE, result.action)

    def test_track_split_freezes(self) -> None:
        result = track_split()
        self.assertEqual(NeutroAction.FREEZE, result.action)
        self.assertEqual(CustomerAgentStatus.FROZEN, result.agent_status)

    def test_ambiguous_hand_to_shelf_motion_recalibrates(self) -> None:
        result = ambiguous_hand_to_shelf_motion()
        self.assertEqual(NeutroAction.RECALIBRATE, result.action)

    def test_basket_pos_visual_mismatch_requests_human_review(self) -> None:
        result = basket_pos_visual_mismatch()
        self.assertEqual(NeutroAction.HUMAN_REVIEW, result.action)
        self.assertGreaterEqual(result.max_dF, 0.85)


if __name__ == "__main__":
    unittest.main()
