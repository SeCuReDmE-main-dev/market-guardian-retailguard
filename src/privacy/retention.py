# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""Law 25-oriented retention defaults for local-first operation."""

from __future__ import annotations

from dataclasses import dataclass


ALLOWED_REVIEW_STATUSES = {
    "review_required",
    "unresolved_contradiction",
    "ambiguous_event",
    "cleared",
}


@dataclass(frozen=True)
class RetentionPolicy:
    raw_frame_persistence_enabled: bool = False
    derived_event_retention_days: int = 30
    case_retention_days: int = 90
    audit_hash_retention_days: int = 365
    incident_register_enabled: bool = True
    operator_audit_enabled: bool = True

    def __post_init__(self) -> None:
        for name in (
            "derived_event_retention_days",
            "case_retention_days",
            "audit_hash_retention_days",
        ):
            value = getattr(self, name)
            if value < 0:
                raise ValueError(f"{name} must be >= 0")

    def assert_status_allowed(self, status: str) -> None:
        if status not in ALLOWED_REVIEW_STATUSES:
            raise ValueError(f"unsupported review status: {status}")
