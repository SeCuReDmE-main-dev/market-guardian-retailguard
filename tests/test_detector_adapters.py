# SPDX-License-Identifier: LicenseRef-SECL-2.0
# Copyright (C) 2026 Jean-Sébastien Beaulieu

import unittest

from src.detectors import CodeProjectDetectorAdapter, Detection, FakeDetectorAdapter


class DetectorAdapterTests(unittest.TestCase):
    def test_fake_detector_returns_metadata_only_detections(self):
        adapter = FakeDetectorAdapter(
            [Detection("d1", "apple", 0.9, (1, 2, 3, 4))]
        )
        detections = adapter.detect("frame-1", zone="aisle")
        self.assertEqual("apple", detections[0].label)
        self.assertEqual((1, 2, 3, 4), detections[0].bbox)

    def test_live_adapter_requires_a_bounded_image_file(self):
        adapter = CodeProjectDetectorAdapter()
        self.assertEqual("http://127.0.0.1:32174", adapter.base_url)
        with self.assertRaisesRegex(ValueError, "approved image file"):
            adapter.detect("missing-frame.jpg", zone="aisle")


if __name__ == "__main__":
    unittest.main()
