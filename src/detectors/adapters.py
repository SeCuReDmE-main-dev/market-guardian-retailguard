# SPDX-License-Identifier: LicenseRef-SECL-2.0
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Optional detector adapters.

The deterministic tests use FakeDetectorAdapter. CodeProjectDetectorAdapter is
kept optional so the core can run without a live CodeProject.AI server.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import mimetypes
from pathlib import Path
from typing import Protocol
import uuid
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
    def __init__(self, base_url: str = "http://127.0.0.1:32174") -> None:
        self.base_url = base_url.rstrip("/")

    def detect(self, frame_ref: str, *, zone: str) -> list[Detection]:
        if not frame_ref:
            raise ValueError("frame_ref is required")
        if not zone:
            raise ValueError("zone is required")
        path = Path(frame_ref)
        if not path.is_file() or not 0 < path.stat().st_size <= 20 * 1024 * 1024:
            raise ValueError("frame_ref must be an approved image file no larger than 20 MiB")
        boundary = f"----retailguard-{uuid.uuid4().hex}"
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        payload = b"".join(
            (
                f'--{boundary}\r\nContent-Disposition: form-data; name="zone"\r\n\r\n{zone}\r\n'.encode(),
                f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="frame{path.suffix}"\r\nContent-Type: {mime}\r\n\r\n'.encode(),
                path.read_bytes(),
                f"\r\n--{boundary}--\r\n".encode(),
            )
        )
        request = Request(
            f"{self.base_url}/v1/vision/detection",
            data=payload,
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "X-CPAI-Forwarded": "true",
            },
            method="POST",
        )
        with urlopen(request, timeout=120) as response:
            body = json.loads(response.read(4 * 1024 * 1024).decode("utf-8"))
        if not isinstance(body, dict) or body.get("success") is not True:
            raise RuntimeError("CodeProject.AI detection did not complete")
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
