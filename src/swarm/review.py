# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Human-review case packaging."""

from __future__ import annotations

from dataclasses import dataclass

from src.privacy import RetentionPolicy


@dataclass(frozen=True)
class ReviewCase:
    case_id: str
    status: str
    evidence_ids: tuple[str, ...]
    summary: str


class HumanReviewAgent:
    def __init__(self, retention_policy: RetentionPolicy | None = None) -> None:
        self.retention_policy = retention_policy or RetentionPolicy()

    def open_case(self, *, case_id: str, status: str, evidence_ids: list[str], summary: str) -> ReviewCase:
        if not case_id:
            raise ValueError("case_id is required")
        if not evidence_ids:
            raise ValueError("at least one evidence_id is required")
        if not summary:
            raise ValueError("summary is required")
        self.retention_policy.assert_status_allowed(status)
        return ReviewCase(
            case_id=case_id,
            status=status,
            evidence_ids=tuple(evidence_ids),
            summary=summary,
        )
