# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Optional detector adapters.

The deterministic tests use FakeDetectorAdapter. CodeProjectDetectorAdapter is
kept optional so the core can run without a live CodeProject.AI server.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Protocol
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class Detection:
    detection_id: str
    label: str
    confidence: float
    bbox: tuple[int, int, int, int]

    def __post_init__(self) -> None:
        if not self.detection_id:
            raise ValueError("detection_id is required")
        if not self.label:
            raise ValueError("label is required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0, 1]")
        if len(self.bbox) != 4:
            raise ValueError("bbox must contain four integers")


class DetectorAdapter(Protocol):
    def detect(self, frame_ref: str, *, zone: str) -> list[Detection]:
        """Return metadata-only detections for a frame reference."""


class FakeDetectorAdapter:
    def __init__(self, detections: list[Detection] | None = None) -> None:
        self._detections = detections or []

    def detect(self, frame_ref: str, *, zone: str) -> list[Detection]:
        if not frame_ref:
            raise ValueError("frame_ref is required")
        if not zone:
            raise ValueError("zone is required")
        return list(self._detections)


class CodeProjectDetectorAdapter:
    def __init__(self, base_url: str = "http://localhost:32168") -> None:
        self.base_url = base_url.rstrip("/")

    def detect(self, frame_ref: str, *, zone: str) -> list[Detection]:
        if not frame_ref:
            raise ValueError("frame_ref is required")
        payload = json.dumps({"frame_ref": frame_ref, "zone": zone}).encode("utf-8")
        request = Request(
            f"{self.base_url}/v1/vision/detection",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            body = json.loads(response.read().decode("utf-8"))
        predictions = body.get("predictions", [])
        detections = []
        for index, item in enumerate(predictions):
            bbox = (
                int(item.get("x_min", 0)),
                int(item.get("y_min", 0)),
                int(item.get("x_max", 0)),
                int(item.get("y_max", 0)),
            )
            detections.append(
                Detection(
                    detection_id=str(item.get("detection_id") or f"cpai-{index}"),
                    label=str(item.get("label", "unknown")),
                    confidence=float(item.get("confidence", 0.0)),
                    bbox=bbox,
                )
            )
        return detections
