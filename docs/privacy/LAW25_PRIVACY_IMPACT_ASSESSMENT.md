# Law 25 Privacy Impact Assessment

Status: v0 scaffold for simulator and design review. This is not legal advice.

## System Purpose

Market Guardian helps small stores reconcile local camera-derived metadata, POS events, inventory movement, and end-of-day cash close results. It creates human-review cases when evidence is contradictory or ambiguous.

## Default Privacy Position

- No face recognition in v1.
- No biometric identification in v1.
- No raw frame persistence by default.
- Temporary anonymous `track_id` only.
- Derived metadata and event hashes are preferred over image or video storage.
- Human operators receive review cases, not automated accusations.

## Personal Information Surfaces

| Surface | Default state | Risk | Control |
|---|---|---|---|
| Camera frames | Ephemeral input only | High if retained or linked to identity. | Not persisted by default; use metadata events. |
| Anonymous track IDs | Temporary session state | Medium if retained too long. | TTL and case-bound retention. |
| POS transactions | Local transaction record | Medium; may link to customer if payment data is present. | Store only item/amount references needed for reconciliation. |
| Inventory events | Product movement metadata | Low to medium. | No customer identity. |
| Operator decisions | Audit trail | Medium; employee information may exist. | Access control and retention policy. |
| Incident register | Compliance record | Medium. | Minimal fields and controlled access. |

## Necessity And Proportionality

The first implementation must prove that metadata-only events are sufficient for:

- basket hypothesis updates;
- POS mismatch detection;
- inventory reconciliation;
- cash close review;
- operator review queue.

Raw frame retention must remain disabled unless a later reviewed deployment requirement explicitly enables it with retention and access controls.

## Safeguards

- Evidence-chain hashes for tamper evidence.
- Bounded review vocabulary.
- No automated enforcement.
- Short-lived customer agents.
- Track-purity freeze when the system might follow the wrong person.
- Source IDs required for every basket item.
- LLM output is explanation only, not authority.

## Open Questions Before Real Store Deployment

- Store signage wording.
- Operator access control model.
- Retention duration approved by accountable privacy role.
- Process for access/correction requests.
- Incident response contact and timeline.
- Whether local footage systems already retain raw video independently.
