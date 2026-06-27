# Reusable Component Map

Status: implementation source map for the first scaffold.

## Component Transfers

| Market Guardian component | Source evidence lane | Reuse pattern | First implementation shape |
|---|---|---|---|
| `NeutroValue` | `neutrosophique` triplet work and private deterministic source repo | Bounded `T/I/F` value with contradiction surface. | `src/neutro/value.py` dataclass with finite `[0,1]` checks. |
| `NeutroAgentScore` | Agent Squad and Aden/Hive retrospectives | Score agent output without flattening unknowns into confidence. | `src/neutro/scoring.py` over observed/inferred/unknown evidence. |
| `NeutroRecalibrationDecision` | Aden/Hive worker and Queen governance | Convert triplet plus divergence into continue, clarify, retry, freeze, review. | Enum plus decision function. |
| `StoreOrchestrator` | Swarm continuity study and Aden/Hive governance | Global supervisor sees all agents but does not hide memory. | Explicit state object and event reducer. |
| `CustomerAgent` | Swarm run-boundary continuity | One anonymous `track_id`, one zone scope, TTL, no identity. | Agent state dataclass with track-purity checks. |
| `MiniYoloWorker` | CodeProject.AI and YOLO case-study surfaces | Bounded detector job, not an autonomous agent. | Adapter interface that accepts ROI/frame metadata and returns detections. |
| `BasketHypothesisAgent` | Evidence-triplet and source-admission work | Basket state is a hypothesis graph backed by evidence IDs. | Item hypothesis records requiring source IDs. |
| `CashCloseAgent` | Current plan plus reconciliation need | End-of-day POS/cash/inventory mismatch gate. | Deterministic calculator with threshold default of `$100`. |
| `HumanReviewAgent` | Safety language from plan and study-case discipline | Package ambiguity, never accuse. | Case packet renderer with allowed status vocabulary. |
| `EvidenceChainLedger` | Quasicrystal metadata-only protection and ledger candidates | Tamper-evident event hashes without raw payload retention. | Hash chain over canonical JSON event metadata. |
| `SensorIntegritySentinel` | YOLO secret-redaction and V.O.T signal-quality patterns | Detect camera, confidence, blur, occlusion, replay, and frozen-frame problems. | Quality metrics fed into `I_system` and drift. |
| `ResourceCostGovernor` | Local-first affordable target | Stop denial-of-wallet and runaway LLM/replay calls. | Budget counters and queue-depth limits. |
| `MachineHealthDriftMonitor` | V.O.T model drift and Quasicrystal readiness reports | Track degradation before decisions become unreliable. | Rolling confidence and false-positive pressure metrics. |
| `Law25RetentionPolicy` | Law 25 plan and Tenebris-style purge | Data minimization, retention, destruction, incident register. | Config object plus tests for default no raw-frame persistence. |

## Code Patterns Worth Reusing

### Strict JSON Contracts

Use explicit JSON validation like the private deterministic source service:

- request body must be object;
- arrays must be arrays;
- required fields must be checked before processing;
- errors must be concrete and 400-level.

### Deterministic Runtime First

Use deterministic CPU-safe behavior first:

- seeded examples;
- no mandatory GPU;
- no mandatory cloud;
- pure Python/standard library where possible for core contracts;
- optional adapters around CodeProject.AI and LLM providers.

### Source Ledger Pattern

Every evidence source should have:

- `source_id`;
- source type;
- event role;
- confidence or quality;
- retention class;
- hash;
- related agent and case IDs.

### Metadata-Only Proof Bundle

For tests and white paper artifacts, emit metadata-only bundles:

- no raw frame bytes;
- no full activity dumps;
- no secrets;
- enough event IDs and hashes to replay the reasoning.

### Additive Integration

Prior study cases show that theory-heavy ideas survive when added as a narrow layer. Therefore the first build must not replace CodeProject.AI, POS, inventory, or operator workflows. It should attach to them.

## First Files To Create After Inventory

```text
src/neutro/value.py
src/neutro/scoring.py
src/neutro/decision.py
src/evidence/events.py
src/evidence/ledger.py
src/swarm/agents.py
src/swarm/orchestrator.py
src/privacy/retention.py
tests/test_concept_inventory.py
tests/test_neutro_scoring.py
tests/test_swarm_guardrails.py
tests/test_privacy_defaults.py
```

## Compatibility Rules

- Public package and docs use `Neutro`.
- Private source names must not appear in this repository.
- CodeProject.AI is an adapter boundary, not a hard runtime requirement for core tests.
- LLM provider calls are optional and must have deterministic fallback.
- Any copied code must be renamed, repathed, simplified, and covered by tests before use.
