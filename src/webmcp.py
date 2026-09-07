# SPDX-License-Identifier: LicenseRef-SECL-2.0
# Copyright (C) 2026 Jean-Sébastien Beaulieu
"""Fail-closed WebMCP registry for the RetailGuard education prototype."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Callable, Mapping

from src.evidence import EvidenceEvent, EvidenceLedger, EventKind
from src.neutro import AgentDivergence, AgentEvidence, EvidenceKind, decide_recalibration, score_agent
from src.simulator.replay import run_checkout_replay
from src.simulator.visual_replay import (
    ambiguous_hand_to_shelf_motion,
    basket_pos_visual_mismatch,
    normal_visual_tracking,
    temporary_occlusion,
    track_split,
)
from src.swarm import CashCloseAgent, HumanReviewAgent, StoreOrchestrator

SCHEMA = "securedme.webmcp.v1"
PRODUCT = "retailguard"


def _property_schema(name: str) -> dict[str, object]:
    if name in {"missedScan", "runtimeConfigured"}:
        return {"type": "boolean"}
    if name in {"cashMismatch", "graphComplexity", "trackPurity", "expected", "counted", "timestampMs", "unsupportedClaims"}:
        return {"type": "number"}
    if name in {"payload", "approval"}:
        return {"type": "object"}
    if name in {"events", "evidence", "evidenceIds"}:
        return {"type": "array", "maxItems": 128}
    return {"type": "string", "minLength": 1, "maxLength": 4096}


@dataclass(frozen=True)
class Tool:
    name: str
    effect: str
    description: str
    required: tuple[str, ...] = ()
    optional: tuple[str, ...] = ()
    available: bool = True

    def descriptor(self) -> dict[str, object]:
        return {
            "name": self.name,
            "mode": self.effect,
            "effect": self.effect,
            "description": self.description,
            "inputSchema": {
                "type": "object",
                "properties": {name: _property_schema(name) for name in (*self.required, *self.optional)},
                "required": list(self.required),
                "additionalProperties": False,
            },
            "outputSchema": {"type": "object"},
            "availability": "available" if self.available else "unavailable",
            "handler": {"kind": "python" if self.available else "unavailable", "module": "src.webmcp"},
            **({} if self.available else {"unavailableReason": "Verified local detector runtime and admitted asset resolver are not configured."}),
        }


DOMAIN_TOOLS = (
    Tool("retailguard_run_checkout_replay", "READ", "Run a synthetic checkout replay with no customer data.", optional=("missedScan", "cashMismatch")),
    Tool("retailguard_run_visual_replay", "READ", "Run one named synthetic visual replay fixture.", ("scenario",)),
    Tool("retailguard_score_agent_evidence", "READ", "Score explicit evidence and contradiction references.", ("evidence",), ("graphComplexity",)),
    Tool("retailguard_decide_recalibration", "READ", "Return a bounded recalibration recommendation from supplied evidence.", ("evidence",), ("graphComplexity", "trackPurity", "unsupportedClaims")),
    Tool("retailguard_reconcile_cash_close", "READ", "Compare declared fixture cash totals for operator review.", ("expected", "counted")),
    Tool("retailguard_score_visual_state", "READ", "Score a synthetic visual state already admitted by the caller.", ("scenario",)),
    Tool("retailguard_open_review_case", "STAGE", "Stage a human review case; never accuse or enforce.", ("caseId", "evidenceIds", "summary")),
    Tool("retailguard_append_evidence_event", "STAGE", "Stage a tamper-evident metadata event in an ephemeral ledger.", ("eventId", "kind", "payload"), ("timestampMs",)),
    Tool("retailguard_verify_evidence_ledger", "READ", "Verify a supplied metadata-only ledger fixture.", ("events",)),
    Tool("retailguard_detect_approved_image", "EXECUTE", "Run approved local image detection when the configured runtime is available.", ("assetRef", "approval", "idempotencyKey"), ("runtimeConfigured", "expectedApprovalId"), False),
)
COMMON_TOOLS = (
    Tool("securedme_companion_context", "READ", "Return the sanitized RetailGuard specialist projection."),
    Tool("securedme_qbit_plan_handoff", "STAGE", "Prepare a Qbit return proposal without changing progression.", ("missionRef", "summary")),
)
TOOLS = DOMAIN_TOOLS + COMMON_TOOLS


def _jsonable(value: object) -> object:
    if isinstance(value, Enum):
        return value.value
    if hasattr(value, "to_dict"):
        return _jsonable(value.to_dict())
    if hasattr(value, "__dataclass_fields__"):
        return _jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def manifest() -> dict[str, object]:
    return {
        "schema": SCHEMA,
        "product": {"slug": PRODUCT, "canonicalStateOwner": "algoquest"},
        "slug": PRODUCT,
        "canonicalStateOwner": "algoquest",
        "tools": [tool.descriptor() for tool in TOOLS],
        "boundaries": {"authority": "Human review owns any decision.", "secrets": "No credentials or raw frames are returned.", "externalWrites": "Only ephemeral staged evidence is produced.", "heroProgression": "AlgoQuest alone owns Hero Book progression.", "biometrics": False, "accusations": False, "enforcement": False, "rawFrameRetention": False},
        "theme": {"source": "assets/landing/secureme.ca-product/education/V.I.S Guardian/desing/stitch_v.i.s_guardian_landing_page/stitch_v.i.s_guardian_landing_page/premium_cyber_heritage/DESIGN.md", "sourceStatus": "verified_stitch_retailguard_mapping"},
    }


def _evidence(payload: Mapping[str, Any]) -> tuple[list[AgentEvidence], list[AgentDivergence]]:
    raw = payload.get("evidence")
    if not isinstance(raw, list):
        raise ValueError("evidence must be an array")
    evidence: list[AgentEvidence] = []
    divergences: list[AgentDivergence] = []
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ValueError(f"evidence[{index}] must be an object")
        if item.get("relation"):
            divergences.append(AgentDivergence(str(item["relation"]), float(item.get("severity", 0.0))))
        else:
            evidence.append(AgentEvidence(EvidenceKind(str(item.get("kind", "unknown"))), str(item.get("eventId", "")), float(item.get("confidence", 1.0))))
    return evidence, divergences


def _visual(payload: Mapping[str, Any]) -> dict[str, object]:
    scenarios: dict[str, Callable[[], object]] = {
        "normal": normal_visual_tracking,
        "temporary_occlusion": temporary_occlusion,
        "track_split": track_split,
        "ambiguous_motion": ambiguous_hand_to_shelf_motion,
        "basket_pos_mismatch": basket_pos_visual_mismatch,
    }
    scenario = payload.get("scenario")
    if scenario not in scenarios:
        raise ValueError("scenario must name a documented synthetic fixture")
    return _jsonable(scenarios[str(scenario)]())  # type: ignore[return-value]


def _score(payload: Mapping[str, Any]) -> dict[str, object]:
    evidence, divergences = _evidence(payload)
    return score_agent(evidence, divergences, graph_complexity=float(payload.get("graphComplexity", 0.0))).to_dict()


def _decision(payload: Mapping[str, Any]) -> dict[str, object]:
    evidence, divergences = _evidence(payload)
    score = score_agent(evidence, divergences, graph_complexity=float(payload.get("graphComplexity", 0.0)))
    return decide_recalibration(score, track_purity=float(payload.get("trackPurity", 1.0)), unsupported_claims=int(payload.get("unsupportedClaims", 0))).to_dict()


def _cash(payload: Mapping[str, Any]) -> dict[str, object]:
    return _jsonable(CashCloseAgent().reconcile(expected_cash=float(payload["expected"]), counted_cash=float(payload["counted"])))  # type: ignore[return-value]


def _review(payload: Mapping[str, Any]) -> dict[str, object]:
    evidence_ids = payload.get("evidenceIds")
    if not isinstance(evidence_ids, list):
        raise ValueError("evidenceIds must be an array")
    case = HumanReviewAgent().open_case(case_id=str(payload.get("caseId", "")), status="review_required", evidence_ids=[str(item) for item in evidence_ids], summary=str(payload.get("summary", "")))
    return {"status": "staged", "durableWrite": False, "case": _jsonable(case), "humanReviewRequired": True}


def _events(payload: Mapping[str, Any]) -> EvidenceLedger:
    raw = payload.get("events")
    if not isinstance(raw, list):
        raise ValueError("events must be an array")
    ledger = EvidenceLedger()
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ValueError(f"events[{index}] must be an object")
        ledger.append(EvidenceEvent(str(item.get("eventId", "")), EventKind(str(item.get("kind", "detection"))), int(item.get("timestampMs", index)), dict(item.get("payload", {}))))
    return ledger


def _append(payload: Mapping[str, Any]) -> dict[str, object]:
    event_payload = payload.get("payload")
    if not isinstance(event_payload, Mapping):
        raise ValueError("payload must be an object")
    ledger = EvidenceLedger()
    entry = ledger.append(EvidenceEvent(str(payload.get("eventId", "")), EventKind(str(payload.get("kind", "detection"))), int(payload.get("timestampMs", 0)), dict(event_payload)))
    return {"status": "staged", "durableWrite": False, "entry": entry.to_dict()}


def _detect(payload: Mapping[str, Any]) -> dict[str, object]:
    if not payload.get("runtimeConfigured"):
        raise RuntimeError("RUNTIME_NOT_CONFIGURED: approved local detector is unavailable")
    approval = payload.get("approval")
    approval_id = approval.get("id") if isinstance(approval, Mapping) else None
    if approval_id != payload.get("expectedApprovalId"):
        raise PermissionError("APPROVAL_REQUIRED: one-use approval is missing or invalid")
    raise RuntimeError("CAPABILITY_DISABLED: live image execution is disabled in the generic WebMCP adapter")


def _context(_: Mapping[str, Any]) -> dict[str, object]:
    return {"schema": "HeroBookPanelState.projection.v1", "product": PRODUCT, "specialist": "Neutro", "canonicalStateOwner": "algoquest", "sanitized": True}


def _handoff(payload: Mapping[str, Any]) -> dict[str, object]:
    if not payload.get("missionRef") or not payload.get("summary"):
        raise ValueError("missionRef and summary are required")
    return {"status": "staged", "missionRef": payload["missionRef"], "summary": payload["summary"], "progressChanged": False, "nextAction": "return_to_qbit_for_human_review"}


HANDLERS: dict[str, Callable[[Mapping[str, Any]], object]] = {
    "retailguard_run_checkout_replay": lambda p: run_checkout_replay(missed_scan=bool(p.get("missedScan", False)), cash_mismatch=float(p.get("cashMismatch", 0.0))),
    "retailguard_run_visual_replay": _visual,
    "retailguard_score_agent_evidence": _score,
    "retailguard_decide_recalibration": _decision,
    "retailguard_reconcile_cash_close": _cash,
    "retailguard_score_visual_state": _visual,
    "retailguard_open_review_case": _review,
    "retailguard_append_evidence_event": _append,
    "retailguard_verify_evidence_ledger": lambda p: {"verified": _events(p).verify()},
    "retailguard_detect_approved_image": _detect,
    "securedme_companion_context": _context,
    "securedme_qbit_plan_handoff": _handoff,
}


def invoke(name: str, payload: Mapping[str, Any] | None = None) -> dict[str, object]:
    if name not in HANDLERS:
        return {"ok": False, "error": {"code": "TOOL_NOT_ALLOWED", "message": "Unknown RetailGuard tool."}}
    try:
        value = HANDLERS[name](payload or {})
    except PermissionError as exc:
        code, _, message = str(exc).partition(":")
        return {"ok": False, "error": {"code": code, "message": message.strip()}}
    except RuntimeError as exc:
        code, _, message = str(exc).partition(":")
        return {"ok": False, "error": {"code": code, "message": message.strip()}}
    except (KeyError, TypeError, ValueError) as exc:
        return {"ok": False, "error": {"code": "INVALID_INPUT", "message": str(exc)}}
    return {"ok": True, "tool": name, "result": _jsonable(value), "trace": {"product": PRODUCT, "sanitized": True}}
