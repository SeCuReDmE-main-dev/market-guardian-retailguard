# Market Guardian Case Study Inventory

Status: first coding action completed.

Source root:

```text
C:\Users\jeans\Desktop\Case study
```

Purpose: extract reusable concepts, implementation patterns, risks, and validation discipline before scaffolding Market Guardian / RetailGuard.

## Inventory Method

This inventory used targeted inspection instead of a blind full read. The case-study root contains roughly 60k files after excluding common dependency and cache folders, so the pass focused on:

- top-level required lanes;
- README, status, report, roadmap, source-ledger, and retrospective documents;
- code paths named around neutrosophic scoring, orchestration, YOLO, privacy, audit, and memory;
- local evidence that includes explicit validation commands or test surfaces.

The root process document `STUDY_CASE_FOUNDATION_PROCESS.md` is the governing method: research first, fit analysis second, RFC/spec before code, implementation in bounded phases, validation, and final retrospective.

## Covered Lanes

| Lane | Observed role | Reusable value for Market Guardian |
|---|---|---|
| `modele` | Technical model and simulator study cases, including FNP-QNN-style runtime work. | Source for deterministic runtime discipline, readiness gates, and future simulator compatibility. |
| `neutrosophique` | Neutrosophic study cases across agent arbitration, swarm worker governance, and RAG evaluation. | Primary source for `Neutro` triplet scoring, consensus, action selection, and host-specific insertion discipline. |
| `Quasicrystal` | Metadata-only protection workflows, CodeProject.AI/YOLO evidence, source admissibility, secret boundaries, and local AI runtime protection. | Source for local perception as metadata, CodeProject.AI mesh direction, evidence admission, redacted telemetry, and no-raw-payload contracts. |
| `swarm` | Swarm orchestration study cases and continuity packet experiments. | Source for agent lifecycle boundaries, explicit context continuity, run-boundary hooks, and helper layers instead of hidden runtime memory. |
| `Memoire` | Agent memory and evolving procedure study cases. | Source for persistent memory, procedural feedback, evolution logs, maintenance agents, and reusable decision history. |
| `mechanique quantique` | Fractal/quantum/neutrogeometry manuscript and research material. | Source for white paper voice, structural math language, and conservative claim boundaries. |
| `biologie` | Biology/life-science study material. | Secondary source for evidence discipline and benchmark-style methodology; not a first build dependency. |
| `STUDY_CASE_FOUNDATION_PROCESS.md` | Root operating method for all case studies. | Mandatory process gate for inventory, source mapping, fit analysis, and phase-scoped implementation. |

## Strongest Reusable Concepts

### 1. Evidence Triplet As A Host-Specific Primitive

The neutrosophic lane proves that truth, indeterminacy, and falsity are useful only when mapped to the host system's real decision surface. In prior work:

- multi-agent systems used triplets for supervisor arbitration;
- swarm runtimes used them for worker report and Queen-style governance;
- RAG evaluation used them as an opt-in evidence metric.

Market Guardian should use the same discipline:

- `CustomerAgent` evaluates one track, not a whole store.
- `BasketHypothesisAgent` evaluates item evidence, not human intent.
- `StoreOrchestrator` fuses scores and chooses continue, recalibrate, freeze, or human review.

### 2. Local Perception As Metadata

The Quasicrystal lane states that YOLO/OCR/frame analysis should produce metadata, not raw media storage. This maps directly to Law 25 and retail safety:

- store detection IDs, bounding boxes, timestamps, confidence, and redacted evidence hashes;
- avoid raw frame persistence by default;
- treat image/video as short-lived input unless an explicit reviewed case requires retention.

### 3. Source Admission And Secret Boundary

Quasicrystal source ledgers and protection matrices use a source -> role -> tag pattern. Market Guardian needs the same idea for retail events:

```text
event source -> evidence role -> admissibility tag -> Neutro score -> case action
```

This prevents an agent from turning weak evidence into a strong claim.

### 4. Swarm Continuity Without Hidden Memory

The Swarm study case warns against hidden runtime memory. The reusable pattern is a narrow continuity packet:

- `track_id`;
- zone scope;
- evidence IDs;
- current basket hypotheses;
- uncertainty state;
- freshness timestamp;
- provenance.

The packet is passed through the orchestrator and validated, not silently injected into agent behavior.

### 5. Procedure Evolution And Memory Feedback

The Memoire lane shows value in procedure feedback and versioned evolution. Market Guardian should evolve operating procedures, not detection facts:

- bad calibration event -> update calibration procedure;
- repeated false positive -> update review threshold or camera-zone guidance;
- operator correction -> append decision feedback;
- failed replay -> record a procedure issue.

### 6. Tenebris-Style Ephemeral Processing

V.O.T-style work gives a useful privacy pattern:

- execute sensitive analysis inside a bounded context;
- destroy raw data quickly;
- retain only metadata, hashes, and audit events;
- log compliance status.

Market Guardian should adapt this pattern for frames and clips.

### 7. Maintainer-Safe Compression

The root study-case process and neutrosophic retrospectives repeatedly show the same rule: compress theory into the smallest useful primitive. For this project:

- do not expose a grand theory engine first;
- implement `NeutroValue`, `AgentEvidence`, `RecalibrationDecision`, and `CaseReviewPacket`;
- make the white paper explain the broader theory after the system can replay examples.

## Concepts To Use Later, Not In The First Build

| Concept | Reason to defer |
|---|---|
| Full GraphRAG or temporal knowledge graph | Useful for long-term case history, but not required for the first simulator. |
| Heavy cloud sandbox execution | Useful for high-risk analysis, but conflicts with the local-first affordable target if made mandatory. |
| Full LLM adjudication | LLMs should explain cases, not govern evidence truth. |
| Production cryptographic claims | Existing work is metadata protection research, not certified cryptography. |
| Biometric identity | Incompatible with the v1 safety and Law 25 posture. |

## Direct Build Implications

The first scaffold should include:

- `src/neutro/` for bounded scoring and recalibration decisions;
- `src/swarm/` for store, customer, mini-YOLO, basket, cash-close, and human-review agents;
- `src/evidence/` for event schemas and tamper-evident hashes;
- `src/privacy/` for retention and Law 25 artifacts;
- `docs/concept_inventory/` as this source map;
- tests that block unsupported item claims, cross-person tracking, private-name leakage, and raw-frame persistence by default.

## Current Decision

Proceed with scaffold only after this inventory package exists and passes its completeness test. The next action is the first build backlog in `FIRST_BUILD_BACKLOG.md`.
