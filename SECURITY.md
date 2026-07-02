# Security Policy

## SecuredMe Education Governance Alignment

- Current phase: pre-alpha / in development.
- Repository license: Secured Educational Cybersecurity License 2.0 (SECL-2.0), local metadata reference LicenseRef-SECL-2.0.
- Official AI-assisted classroom routes: Codex/OpenAI and Antigravity/Gemini only.
- Do not add Ollama Cloud, uncensored local AI, raw-token student flows, or unknown agent providers as official school routes.
- Cybersecurity, fraud-awareness, protection, or abuse-prevention behavior must stay defensive and supervised.
- Preserve human-review boundaries; do not claim production, clinical, regulatory, enforcement, safety-critical, or autonomous authority readiness.
- Private modified copies, broken forks, and unreviewed rewrites are not a maintainer support obligation.


Market Guardian / RetailGuard is a safety-sensitive local retail protection system. Security issues can affect people, store operators, cameras, POS data, inventory records, AI agents, and privacy obligations.

## Current Support Status

The project is pre-release and unstable. There are no supported production versions yet.

Do not deploy this repository as a production enforcement system without an independent security, privacy, and legal review.

## Responsible Disclosure

Please report security issues privately to the project maintainer before public disclosure. If GitHub Security Advisories are enabled for the public repository, use that path first. If not, use a private maintainer contact channel and include enough detail to reproduce the issue without exposing real customer data or camera footage.

Useful report content:

- affected file, module, endpoint, or workflow;
- reproduction steps;
- expected behavior;
- observed behavior;
- impact;
- whether real personal information, camera frames, POS records, or credentials were exposed;
- proposed fix, if known.

Do not include raw camera frames, biometric identifiers, secrets, customer identities, or real POS records in a public issue.

## Non-Autonomous Safety Boundary

The system must not make autonomous enforcement decisions.

Machine output can request review, identify unresolved contradiction, describe evidence divergence, or highlight ambiguity. A human operator remains responsible for interpretation and action.

## Privacy And Law 25 Posture

The version 1 posture is:

- no face recognition;
- no biometric identification;
- no identity matching;
- no raw-frame persistence by default;
- anonymous temporary `track_id` instead of personal identity;
- retention and destruction controls;
- operator audit trail;
- incident register;
- privacy impact assessment before production use.

Report a security issue if a change weakens these defaults, stores raw frames silently, creates identity linkage, extends retention without a policy, or bypasses the operator audit trail.

## Model And Agent Security

Report issues involving:

- prompt injection that changes safety rules;
- agent output that is not evidence-bound;
- basket updates without evidence references;
- cross-person track contamination;
- detector spoofing;
- replay poisoning;
- ledger tampering;
- cash closeout manipulation;
- cost-governor bypass;
- model drift that hides ambiguity;
- logs that expose sensitive camera, POS, or operator data.

## Secrets And Credentials

Never commit:

- API keys;
- POS credentials;
- camera passwords;
- model provider tokens;
- customer data;
- raw camera frames;
- production logs with personal information.

Use local environment variables or deployment-specific secret storage. Keep `.env` files out of version control.

## Dependency And Model Supply Chain

Before production use, integrators must validate:

- Python dependency licenses and vulnerabilities;
- YOLO model source and license;
- CodeProject.AI module terms;
- dataset rights;
- cloud LLM endpoint terms;
- camera and POS vendor terms;
- Quebec Law 25 obligations and any other applicable law.

## Public Issues

Do not open public issues containing exploit details, live camera information, credentials, real customer records, or enough operational detail to compromise a store. Use private disclosure first.
