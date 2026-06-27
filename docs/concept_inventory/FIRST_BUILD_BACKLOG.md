# First Build Backlog

Status: executable order after concept inventory.

## Gate 0 - Inventory Completeness

Goal: prove the first action was completed before scaffold.

Tasks:

1. Create the five concept inventory documents.
2. Add a standard-library test for inventory completeness.
3. Run the test.
4. Confirm no reserved private naming appears in public repo files.

Acceptance:

- `docs/concept_inventory/CASE_STUDY_INVENTORY.md` exists.
- `docs/concept_inventory/REUSABLE_COMPONENT_MAP.md` exists.
- `docs/concept_inventory/DO_NOT_REUSE_RISKS.md` exists.
- `docs/concept_inventory/NEUTRO_IMPLEMENTATION_SOURCE_MAP.md` exists.
- `docs/concept_inventory/FIRST_BUILD_BACKLOG.md` exists.
- Required lanes are named.
- No scaffold starts until this gate passes.

## Gate 1 - Minimal Python Package

Goal: create the deterministic core without runtime dependencies.

Tasks:

1. Create `src/neutro/value.py`.
2. Create `src/neutro/scoring.py`.
3. Create `src/neutro/decision.py`.
4. Add tests for bounds, contradiction, `dF`, `D_f_hat`, and deterministic decisions.

Acceptance:

- Tests run with standard Python plus pytest if available.
- No CodeProject.AI, LLM, database, or cloud dependency is required.

## Gate 2 - Evidence And Ledger

Goal: prevent hallucinated basket claims.

Tasks:

1. Create event dataclasses for detection, POS, inventory, synthetic replay, and cash close.
2. Add canonical JSON serialization.
3. Add tamper-evident hash chain.
4. Reject basket updates that lack an evidence ID.

Acceptance:

- Unsupported item claims fail tests.
- Ledger hash changes when event metadata changes.
- Raw frame bytes are not accepted in default metadata events.

## Gate 3 - Swarm Guardrails

Goal: spawn one bounded customer agent per anonymous track.

Tasks:

1. Create `CustomerAgent`.
2. Create `MiniYoloWorker` interface.
3. Create `BasketHypothesisAgent`.
4. Create `StoreOrchestrator`.
5. Add track-purity and TTL checks.

Acceptance:

- A customer-entered event spawns one scoped agent.
- Track-purity drop freezes the agent.
- Same item claimed by two agents creates a divergence.
- Agent states remain auditable and serializable.

## Gate 4 - Privacy Defaults

Goal: enforce Law 25-aligned defaults before UI or live camera work.

Tasks:

1. Create retention policy.
2. Create incident register schema.
3. Create operator audit event schema.
4. Add default no-raw-frame persistence test.

Acceptance:

- Raw frame persistence is false by default.
- Evidence events store metadata and hashes, not image bytes.
- Human-review cases use non-accusation statuses.

## Gate 5 - CodeProject.AI Adapter

Goal: connect to local YOLO without making it mandatory for tests.

Tasks:

1. Create detector adapter interface.
2. Create fake detector for replay tests.
3. Create CodeProject.AI detector adapter with `localhost:32168` config.
4. Add optional live smoke test marker.

Acceptance:

- Unit tests pass without CodeProject.AI running.
- Optional smoke test can be skipped cleanly.
- Detector outputs are converted into evidence events.

## Gate 6 - Simulator Replay

Goal: prove end-to-end behavior with synthetic store days.

Tasks:

1. Create synthetic store day generator.
2. Add normal checkout replay.
3. Add missed scan replay.
4. Add returned item replay.
5. Add occlusion replay.
6. Add `$100+` cash mismatch replay.

Acceptance:

- The system opens review cases only on contradiction or high ambiguity.
- It never emits confirmed-accusation language.
- Replay output produces metadata-only proof bundles.

## Gate 7 - Dashboard And White Paper Seed

Goal: show operator value without overclaiming.

Tasks:

1. Build basic dashboard only after replay core passes.
2. Add AI Builder Declaration.
3. Add Law 25 status panel.
4. Add white paper source ledger.

Acceptance:

- Dashboard displays review, ambiguity, machine health, and privacy status.
- White paper claims link to local evidence or marked hypotheses.
