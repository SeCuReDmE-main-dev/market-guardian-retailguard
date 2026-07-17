# SPDX-License-Identifier: LicenseRef-SECL-2.0
# Copyright (C) 2026 Jean-Sébastien Beaulieu

"""AlgoQuest/Qbit Education adapter hook for Market Guardian."""

APP_SLUG = "market-guardian"
HUB_SLUG = "algoquest"
OUTBOX_SCHEMA = "securedme.education.student-learning-event.v1"


def build_learning_event_stub(artifact_ref: str, *, score: float = 93) -> dict:
    return {
        "schema": OUTBOX_SCHEMA,
        "app_slug": APP_SLUG,
        "artifact_ref": artifact_ref,
        "skill_area": "market_risk_reasoning",
        "difficulty_band": "beginner",
        "score": score,
        "threshold": 93,
        "attempt_count": 1,
        "blocked_reason": "",
        "next_step_hint": "Open AlgoQuest to turn this risk signal into a safe reasoning exercise.",
        "qbit_help_accepted": False,
        "risk_flags": [],
        "contract_version": "v1",
        "raw_secret_stored": False,
        "dry_run": True,
    }


def build_review_case_learning_event(case_id: str, *, status: str, score: float = 93) -> dict:
    """Build a secret-safe AlgoQuest pointer for a human-review case."""

    event = build_learning_event_stub(f"{APP_SLUG}:review-case:{case_id}", score=score)
    event["blocked_reason"] = "human_review_needed" if status else ""
    event["risk_flags"] = ["human_review"] if status else []
    event["next_step_hint"] = "Open AlgoQuest to turn this market-review case into a safe reasoning exercise."
    return event
