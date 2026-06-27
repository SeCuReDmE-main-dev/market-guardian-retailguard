# Integration Protocol

An integration decision is required when an idea from Jean-Sébastien Construction Space and an engineering artifact from Codex Construction Space become part of the shared Market Guardian / RetailGuard tool.

Minimum fields:

- `decision_id`
- `human_artifact_id`
- `codex_artifact_id`
- `accepted_output`
- `rationale`
- `timestamp_ms`

Rules:

- Do not integrate an artifact without a rationale.
- Do not integrate AI-origin output as autonomous authority.
- Do not integrate personal identity, biometric, or raw-frame requirements.
- Do not integrate operator-facing accusation language.
- Preserve the public naming boundary: Market Guardian / RetailGuard, Neutro, V.I.S Guardian, and V.O.T Guardian.

This protocol is implemented by `src/construction/integration.py`.
