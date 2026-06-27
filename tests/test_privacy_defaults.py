# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

import unittest
from pathlib import Path

from src.privacy import ALLOWED_REVIEW_STATUSES, RetentionPolicy


ROOT = Path(__file__).resolve().parents[1]


class PrivacyDefaultsTests(unittest.TestCase):
    def test_raw_frame_persistence_is_disabled_by_default(self):
        policy = RetentionPolicy()
        self.assertFalse(policy.raw_frame_persistence_enabled)
        self.assertTrue(policy.incident_register_enabled)
        self.assertTrue(policy.operator_audit_enabled)

    def test_review_status_vocabulary_is_bounded(self):
        policy = RetentionPolicy()
        for status in ALLOWED_REVIEW_STATUSES:
            policy.assert_status_allowed(status)
        with self.assertRaises(ValueError):
            policy.assert_status_allowed("confirmed_accusation")

    def test_privacy_artifacts_exist(self):
        for path in [
            "docs/privacy/LAW25_PRIVACY_IMPACT_ASSESSMENT.md",
            "docs/privacy/DATA_INVENTORY.yml",
            "docs/privacy/RETENTION_DESTRUCTION_POLICY.md",
            "docs/privacy/INCIDENT_REGISTER.jsonl",
            "docs/privacy/OPERATOR_AUDIT_LOG_SCHEMA.md",
        ]:
            self.assertTrue((ROOT / path).is_file(), path)


if __name__ == "__main__":
    unittest.main()
