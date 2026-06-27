# Market Guardian / RetailGuard

Market Guardian / RetailGuard is an open source, local-first retail protection system for small markets, depanneurs, grocery stores, and local food operators. The project exists to show that cybersecurity is not only a web problem. Local stores also have security surfaces: cameras, point-of-sale events, inventory movement, cash closeout, operator workflows, model prompts, detector output, and human review.

The goal is not to build an autonomous accusation machine. The goal is to reconcile evidence, measure contradiction, preserve privacy, and hand a clear review package to a human operator when the system cannot explain what happened with enough confidence.

This repository is currently a builder-facing foundation until the public website and polished product documentation exist.

## Status

This project is unstable and under active construction.

Pull requests are not accepted yet. The architecture, safety model, privacy controls, and public documentation still need to harden before outside contributions can be reviewed responsibly.

Current foundation:

- concept inventory from the local case-study corpus;
- Neutro mathematical scoring primitives;
- deterministic evidence events and hash-chain ledger;
- customer-scoped swarm agents;
- basket evidence guardrails;
- cash closeout reconciliation;
- Law 25 oriented privacy documents;
- simulator replay scenarios;
- unit tests for core guardrails.

## Mission

Small stores face loss, inventory drift, cash mismatches, and operational mistakes without the budget for enterprise retail-protection tooling. A local-first system should let them use existing cameras, POS exports, inventory data, and affordable AI endpoints while keeping human review in control.

Market Guardian / RetailGuard treats the store as a local cyber-physical system:

- cameras produce visual observations;
- detectors produce bounded facts;
- POS produces transaction events;
- inventory systems produce stock movement;
- cash closeout produces end-of-day balances;
- agents maintain scoped hypotheses;
- Neutro measures truth, contradiction, uncertainty, and divergence;
- human operators receive review-required cases, not verdicts.

## Core Architecture

The intended foundation is CodeProject.AI Server plus YOLO-compatible detection. CodeProject.AI is used as the local vision/backend anchor because it can run near the cameras and expose detector responses through a service boundary.

Neutro is the public name for the neutrosophic swarm governor. It is responsible for keeping agent output disciplined, evidence-bound, and contradiction-aware.

The build order is:

1. simulator and specification;
2. CodeProject.AI-compatible module patterns;
3. dashboard and operator review surface;
4. dataset loaders and replay tools;
5. NSS white paper dossier.

LLMs are not the authority for facts. Deterministic reconciliation is the authority. LLMs may explain, summarize, or help review through Codex, Antigravity/Gemini, Ollama cloud, or compatible endpoints, but only when the underlying evidence chain is available.

## Swarm Model

The system uses scoped agents instead of one global free-form model:

- `StoreOrchestrator` supervises cameras, POS, inventory, cash, privacy, and machine health.
- `CustomerAgent` is spawned for one anonymous `track_id` when a customer enters.
- `MiniYoloWorker` runs bounded detector work for shelf, basket, checkout, or exit zones.
- `BasketHypothesisAgent` maintains possible basket state with references to evidence.
- `CashCloseAgent` reconciles end-of-day cash, POS, and inventory movement.
- `HumanReviewAgent` packages ambiguity for a human operator.

Each customer agent must stay attached to one anonymous track. If track purity fails, the agent freezes and escalates the case for human review.

## Neutro Guardrails

Agent output is restricted to:

- `observed`;
- `inferred`;
- `unknown`.

A basket item cannot be added without one of these references:

- `detection_id`;
- `pos_id`;
- `inventory_event_id`;
- `synthetic_replay_id`.

The system tracks:

- `T_system`;
- `I_system`;
- `F_system`;
- `dF`;
- `D_f_hat`.

The hierarchy is preserved:

`I -> I_system^S -> D_f -> dF -> i_fractal`

The purpose is to keep uncertainty structured instead of letting a model flatten ambiguity into a confident story.

## Retail Workflows

Normal workflow:

1. A customer enters the store.
2. An anonymous track is created.
3. A scoped customer agent is spawned.
4. Detector events, shelf events, basket hypotheses, POS scans, and checkout events are reconciled.
5. If evidence aligns, no review package is created.
6. If evidence conflicts or ambiguity rises, the human operator receives a review-required case.

Cash closeout workflow:

1. POS totals, cash drawer count, and inventory movement are loaded.
2. The cash agent computes the mismatch.
3. Small mismatch cases remain operational notes.
4. A threshold such as `$100+` triggers a deeper evidence review.
5. The system packages ambiguous intervals and evidence references for human review.

Replay scenarios currently covered include normal checkout, missed scan, duplicate scan, returned item, occlusion, track split, ambiguous item, and cash mismatch.

## Law 25 And Privacy Defaults

This project is designed with Quebec Law 25 posture in mind. It is not legal advice and must be reviewed by qualified counsel before production deployment.

Version 1 defaults:

- no face recognition;
- no biometric identification;
- no identity tracking;
- no raw-frame persistence by default;
- temporary anonymous `track_id` instead of personal identity;
- data minimization;
- retention and destruction planning;
- operator audit trail;
- incident register;
- privacy impact assessment;
- human review for ambiguous cases.

Privacy documents live under `docs/privacy/`.

## Safety Language

Operator-facing language must stay non-accusatory. Preferred terms:

- `review required`;
- `unresolved contradiction`;
- `ambiguous event`;
- `cash mismatch review`;
- `evidence divergence`.

The system must not tell staff that a person committed an act. It can only say that the evidence does not reconcile and that a human needs to review the case.

## Machine Protection

This repository also treats the AI structure itself as something that needs protection.

Machine-protection functions planned in the architecture:

- `model_prompt_integrity_firewall`;
- `sensor_integrity_sentinel`;
- `evidence_chain_ledger`;
- `resource_cost_governor`;
- `machine_health_drift_monitor`.

These functions protect the machine layer from prompt injection, sensor spoofing, corrupted evidence, uncontrolled cost, model drift, and degraded detector quality.

## Repository Layout

- `src/neutro/` contains mathematical scoring and decision primitives.
- `src/evidence/` contains evidence events and ledger structures.
- `src/swarm/` contains customer, basket, cash, review, and orchestrator agents.
- `src/detectors/` contains detector adapters.
- `src/simulator/` contains deterministic replay scenarios.
- `src/privacy/` contains retention helper code.
- `docs/concept_inventory/` contains the first mandatory case-study inventory.
- `docs/privacy/` contains Law 25 oriented governance artifacts.
- `tests/` contains the current unit test suite.

## Development Commands

Run tests:

```powershell
python -m unittest discover -s tests -v
```

Compile-check source and tests:

```powershell
python -m compileall -q src tests
```

Optional future live CodeProject.AI check:

```powershell
Invoke-WebRequest http://localhost:32168
```

## License

This project is licensed under the GNU Affero General Public License, version 3 or later:

`AGPL-3.0-or-later`

The license is intentionally strong copyleft because this system is networked, local-server oriented, and safety-sensitive. Improvements that are deployed as services should remain available to the people relying on the system.

Attribution:

Jean-Sébastien Beaulieu  
ORCID: https://orcid.org/0009-0007-2904-0443

See `LICENSE`, `NOTICE`, and `LICENSE_POLICY.md`.

## Public Repo Rollout

This repository does not automatically change any other public repository. Other repositories must be inventoried first:

- public/private status;
- whether the tool is original to the author;
- existing license;
- dependency licenses;
- public documentation impact;
- recommended action.

AGPL plus `NOTICE` should only be applied to another repository after explicit approval for that specific repository.

## Contribution Policy

Pull requests are not accepted yet.

The current focus is to stabilize the core architecture, tests, privacy posture, and white paper foundation before opening contribution intake. See `CONTRIBUTING.md`.
