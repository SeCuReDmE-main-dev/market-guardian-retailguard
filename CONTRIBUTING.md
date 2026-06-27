# Contributing

Market Guardian / RetailGuard is not accepting pull requests yet.

The project is still stabilizing its architecture, privacy posture, safety language, licensing, and evidence model. Reviewing outside patches before those foundations are stable would create avoidable risk for a safety-sensitive system.

## Current Policy

- Pull requests are closed until contribution intake opens.
- Security reports should follow `SECURITY.md`.
- Licensing questions should follow `LICENSE_POLICY.md`.
- Public discussion must avoid real customer data, camera frames, credentials, POS records, and personally identifying information.

## Local Validation

Before any future contribution path opens, project-owned changes should pass:

```powershell
python -m unittest discover -s tests -v
python -m compileall -q src tests
```

## Future Contribution Gate

Contribution intake should only open after:

- the public API surface is stable enough to review;
- privacy and retention policies are settled;
- the CodeProject.AI integration boundary is documented;
- test fixtures avoid personal information;
- dependency licensing has been inventoried;
- safety-language rules are enforced by tests;
- the maintainer has published a review process.
