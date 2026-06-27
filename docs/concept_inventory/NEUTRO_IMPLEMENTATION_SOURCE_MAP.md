# Neutro Implementation Source Map

Status: naming-safe source map for the public `Neutro` layer.

## Public Name

The public model/layer name is:

```text
Neutro
```

Reserved private names are not used in this repository. Any source material from private research code must be renamed and repathed before it becomes public-facing code.

## Required Python Layout

Preferred first layout:

```text
src/neutro/
src/
  neutro/
    __init__.py
    value.py
    scoring.py
    decision.py
    contract.py
  evidence/
    __init__.py
    events.py
    ledger.py
  swarm/
    __init__.py
    agents.py
    orchestrator.py
  privacy/
    __init__.py
    retention.py
```

## Neutro Core Objects

| Object | Responsibility |
|---|---|
| `NeutroValue` | Bounded `T_system`, `I_system`, `F_system` triple plus contradiction helper. |
| `LocalTension` | `dF` contribution from one conflicting relation. |
| `FractalComplexity` | `D_f_hat` normalized complexity value. |
| `AgentEvidence` | Observed/inferred/unknown evidence record tied to event IDs. |
| `AgentDivergence` | Structured disagreement between camera, POS, inventory, basket, or cash evidence. |
| `NeutroAgentScore` | Combined score for one agent at one time. |
| `NeutroRecalibrationDecision` | Continue, recalibrate, freeze, split, merge, quarantine, or human review. |
| `NeutroContract` | Public schema and invariant list for APIs and tests. |

## Mathematical Boundary

Keep the hierarchy:

```text
I -> I_system^S -> D_f -> dF -> i_fractal
```

Use it as a design hierarchy, not as an unsupported proof claim.

Practical mapping:

- `I`: raw indeterminacy in an event.
- `I_system^S`: system-level indeterminacy over an agent or case.
- `D_f`: structural/fractal dimension concept reserved for documented math.
- `dF`: local contradiction/tension from a specific relation.
- `i_fractal`: local unresolved detail in a recursive event structure.

## API Contract Draft

```text
GET  /v1/neutro/contract
POST /v1/neutro/score-agent
POST /v1/neutro/recalibrate
POST /v1/swarm/customer-entered
POST /v1/swarm/detection-event
GET  /v1/swarm/agents/{track_id}
```

## Agent Evidence Rules

An agent output must be:

- `observed`: directly backed by a detection, POS, inventory, synthetic replay, or cash event.
- `inferred`: derived from observed evidence and marked with uncertainty.
- `unknown`: unresolved and not usable as a claim.

Required reference rule:

```text
No basket item can be added without detection_id, pos_id, inventory_event_id, or synthetic_replay_id.
```

## Divergence Inputs

The first implementation should score divergence from:

- missing POS item;
- item seen but not paid;
- item paid but not seen;
- duplicate POS scan;
- item return to shelf;
- track purity drop;
- camera occlusion;
- detection confidence collapse;
- same item claimed by two agents;
- cash close mismatch above threshold.

## Repathing Requirements

When adapting source patterns:

- rewrite package imports to `src.neutro` or project-local equivalent;
- rewrite Flask/FastAPI route names to `/v1/neutro/...`;
- rewrite tests to public names;
- remove broad service dependencies from the deterministic core;
- preserve only bounded, tested behavior.

## First Validation Rules

The first tests must prove:

- all `NeutroValue` components stay finite and in `[0,1]`;
- contradiction and local tension are deterministic;
- unsupported item claims are rejected;
- cross-person tracking freezes an agent;
- public files do not contain reserved private names;
- raw-frame retention is off by default.
