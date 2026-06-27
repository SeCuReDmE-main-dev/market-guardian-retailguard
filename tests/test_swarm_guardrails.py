# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

import unittest

from src.swarm import CustomerAgentStatus, StoreOrchestrator


class SwarmGuardrailTests(unittest.TestCase):
    def test_customer_entered_spawns_one_agent_per_track(self):
        orchestrator = StoreOrchestrator()
        first = orchestrator.customer_entered("track-1", "entry", 0)
        second = orchestrator.customer_entered("track-1", "entry", 10)
        self.assertIs(first, second)
        self.assertEqual(1, len(orchestrator.agents))

    def test_basket_item_requires_evidence_id(self):
        orchestrator = StoreOrchestrator()
        orchestrator.customer_entered("track-1", "aisle-1", 0)
        with self.assertRaises(ValueError):
            orchestrator.add_basket_item(
                "track-1",
                sku="sku-1",
                label="apple",
                evidence_id="",
                confidence=0.8,
            )

    def test_track_purity_drop_freezes_agent(self):
        orchestrator = StoreOrchestrator()
        agent = orchestrator.customer_entered("track-1", "entry", 0)
        orchestrator.update_track_purity("track-1", 0.4)
        self.assertEqual(CustomerAgentStatus.FROZEN, agent.status)


if __name__ == "__main__":
    unittest.main()
