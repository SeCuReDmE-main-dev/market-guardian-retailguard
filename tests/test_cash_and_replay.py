# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

import unittest

from src.simulator import run_checkout_replay
from src.swarm import CashCloseAgent, HumanReviewAgent


class CashAndReplayTests(unittest.TestCase):
    def test_cash_close_threshold(self):
        agent = CashCloseAgent()
        self.assertFalse(agent.reconcile(expected_cash=100.0, counted_cash=150.0).requires_review)
        self.assertTrue(agent.reconcile(expected_cash=100.0, counted_cash=201.0).requires_review)

    def test_review_case_status_is_bounded(self):
        agent = HumanReviewAgent()
        case = agent.open_case(
            case_id="case-1",
            status="ambiguous_event",
            evidence_ids=["event-1"],
            summary="Operator review needed.",
        )
        self.assertEqual("ambiguous_event", case.status)
        with self.assertRaises(ValueError):
            agent.open_case(
                case_id="case-2",
                status="bad_status",
                evidence_ids=["event-1"],
                summary="Operator review needed.",
            )

    def test_normal_checkout_replay_has_no_review_case(self):
        result = run_checkout_replay()
        self.assertTrue(result.ledger_verified)
        self.assertEqual(1, result.basket_items)
        self.assertEqual(0, len(result.review_cases))

    def test_missed_scan_replay_opens_review_case(self):
        result = run_checkout_replay(missed_scan=True)
        self.assertTrue(result.ledger_verified)
        self.assertEqual(1, len(result.review_cases))

    def test_cash_mismatch_opens_review_case(self):
        result = run_checkout_replay(cash_mismatch=150.0)
        self.assertTrue(result.cash_requires_review)
        self.assertEqual(1, len(result.review_cases))


if __name__ == "__main__":
    unittest.main()
