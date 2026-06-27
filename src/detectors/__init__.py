# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Detector adapter boundaries."""

from .adapters import CodeProjectDetectorAdapter, Detection, DetectorAdapter, FakeDetectorAdapter

__all__ = ["CodeProjectDetectorAdapter", "Detection", "DetectorAdapter", "FakeDetectorAdapter"]
