# Retention And Destruction Policy

Status: v0 default policy for simulator and early development.

## Defaults

| Data class | Default retention |
|---|---|
| Raw frames | Not persisted. |
| Derived detection events | 30 days. |
| Active review cases | 90 days. |
| Audit hashes | 365 days. |
| Anonymous track state | Destroyed at session TTL unless attached to a review case. |
| Incident register | Kept according to privacy/accountability requirements. |

## Destruction Events

Every destruction action should produce metadata:

- `destruction_id`;
- `data_class`;
- `scope_id`;
- `timestamp_ms`;
- `operator_or_system`;
- `result`;
- `audit_hash`.

## Non-Goals

- This policy does not override a store's separate camera DVR retention.
- This policy does not authorize biometric identification.
- This policy does not authorize raw frame persistence by default.
