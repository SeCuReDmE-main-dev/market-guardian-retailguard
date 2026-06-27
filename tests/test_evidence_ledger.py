# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

import unittest

from src.evidence import EvidenceEvent, EvidenceLedger, EventKind


class EvidenceLedgerTests(unittest.TestCase):
    def test_ledger_hash_chain_verifies(self):
        ledger = EvidenceLedger()
        ledger.append(EvidenceEvent("d1", EventKind.DETECTION, 100, {"label": "apple"}))
        ledger.append(EvidenceEvent("pos1", EventKind.POS, 200, {"sku": "apple"}))
        self.assertTrue(ledger.verify())
        self.assertNotEqual(ledger.entries[0].entry_hash, ledger.entries[1].entry_hash)

    def test_raw_frame_metadata_is_rejected_by_default(self):
        with self.assertRaises(ValueError):
            EvidenceEvent("d1", EventKind.DETECTION, 100, {"raw_frame": "bytes"})


if __name__ == "__main__":
    unittest.main()
