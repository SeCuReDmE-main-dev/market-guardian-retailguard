# Decisions

## 2026-06-27 - Public License

Decision: use `AGPL-3.0-or-later`.

Reason: the project is a network-capable local service and needs strong copyleft protection for deployed improvements.

Rejected: custom open source license for now.

Revisit: only after legal review and only if a custom license is still necessary.

## 2026-06-27 - Public Repository Name

Decision: publish as `market-guardian-retailguard`.

Reason: clear project identity, no private research-name exposure, and understandable to outside readers.

## 2026-06-27 - CI Baseline

Decision: run `unittest` and `compileall` in GitHub Actions.

Reason: the first public gate should prove that guardrail tests and source syntax remain valid on every push.
