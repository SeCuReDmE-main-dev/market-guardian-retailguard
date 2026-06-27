# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

import unittest

from src.detectors import Detection, FakeDetectorAdapter


class DetectorAdapterTests(unittest.TestCase):
    def test_fake_detector_returns_metadata_only_detections(self):
        adapter = FakeDetectorAdapter(
            [Detection("d1", "apple", 0.9, (1, 2, 3, 4))]
        )
        detections = adapter.detect("frame-1", zone="aisle")
        self.assertEqual("apple", detections[0].label)
        self.assertEqual((1, 2, 3, 4), detections[0].bbox)


if __name__ == "__main__":
    unittest.main()
