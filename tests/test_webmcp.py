# SPDX-License-Identifier: LicenseRef-SECL-2.0
# Copyright (C) 2026 Jean-Sébastien Beaulieu

from src.webmcp import DOMAIN_TOOLS, TOOLS, invoke, manifest


def test_catalogue_is_normalized_and_unique() -> None:
    assert manifest()["slug"] == "retailguard"
    assert len(DOMAIN_TOOLS) == 10
    assert len(TOOLS) == len({tool.name for tool in TOOLS}) == 12
    assert all(tool["inputSchema"]["additionalProperties"] is False for tool in manifest()["tools"])
    assert all(set(tool["inputSchema"]["required"]) <= set(tool["inputSchema"]["properties"]) for tool in manifest()["tools"])


def test_checkout_fixture_executes_without_customer_data() -> None:
    response = invoke("retailguard_run_checkout_replay", {"missedScan": True})
    assert response["ok"] is True
    assert response["result"]["ledger_verified"] is True


def test_review_case_is_staged_not_persisted() -> None:
    response = invoke("retailguard_open_review_case", {"caseId": "fixture-case", "evidenceIds": ["fixture-event"], "summary": "Synthetic mismatch needs review."})
    assert response["ok"] is True
    assert response["result"]["durableWrite"] is False
    assert response["result"]["humanReviewRequired"] is True


def test_detector_fails_closed_without_runtime() -> None:
    response = invoke("retailguard_detect_approved_image", {"assetRef": "fixture:image", "approvalId": "approval", "idempotencyKey": "once"})
    assert response["ok"] is False
    assert response["error"]["code"] == "RUNTIME_NOT_CONFIGURED"


def test_qbit_handoff_never_advances_progress() -> None:
    response = invoke("securedme_qbit_plan_handoff", {"missionRef": "mission:fixture", "summary": "Bounded review complete."})
    assert response["result"]["progressChanged"] is False
