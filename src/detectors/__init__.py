# SPDX-License-Identifier: LicenseRef-SECL-2.0
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Detector adapter boundaries."""

from .adapters import CodeProjectDetectorAdapter, Detection, DetectorAdapter, FakeDetectorAdapter

__all__ = ["CodeProjectDetectorAdapter", "Detection", "DetectorAdapter", "FakeDetectorAdapter"]
