# Operator Audit Log Schema

Status: v0.

Every operator action on a review case should be logged as metadata.

```json
{
  "audit_event_id": "audit-001",
  "timestamp_ms": 0,
  "operator_id": "local-operator",
  "case_id": "case-001",
  "action": "open_case",
  "status_before": "review_required",
  "status_after": "ambiguous_event",
  "evidence_ids": ["event-001"],
  "notes_hash": "sha256-or-empty",
  "entry_hash": "sha256"
}
```

Allowed review statuses:

- `review_required`
- `unresolved_contradiction`
- `ambiguous_event`
- `cleared`

The audit log should not contain raw images, raw video, payment card details, or private notes in clear text.
