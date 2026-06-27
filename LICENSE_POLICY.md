# License Policy

This repository uses:

`AGPL-3.0-or-later`

## Why AGPL

Market Guardian / RetailGuard is intended to run as a local server, camera/POS reconciliation service, or network-accessible retail-protection tool. A permissive license would allow someone to deploy modified versions as a service without sharing improvements. The GNU Affero General Public License closes that network-service gap and keeps core improvements available to store operators, researchers, and the open source community.

AGPL also matches the safety posture of this project. If a deployed version changes privacy behavior, agent guardrails, detector assumptions, or review language, the source changes should remain inspectable.

## SPDX Identifier

The project license identifier is:

`AGPL-3.0-or-later`

Project-owned source files should include:

```text
SPDX-License-Identifier: AGPL-3.0-or-later
```

## Attribution

Author and project originator:

Jean-Sébastien Beaulieu  
ORCID: https://orcid.org/0009-0007-2904-0443

Attribution belongs in `NOTICE`, `README.md`, and source copyright headers. It is not implemented as a custom license restriction.

## Why Not A Custom License Now

SPDX supports custom license references through `LicenseRef-*` expressions, but a custom license is not automatically recognized as open source. The Open Source Initiative reviews licenses separately, and unreviewed custom text can create uncertainty for users, contributors, researchers, and downstream operators.

For this repository, recognized open source matters more than custom license branding. The custom-license path is deferred.

## Other Public Repositories

This policy does not automatically relicense other repositories.

Before applying AGPL plus `NOTICE` elsewhere, create an inventory:

- list public repositories under the relevant GitHub account;
- classify which repositories are original tools by the author;
- record current license state;
- record dependency and model licenses;
- record public/private status;
- identify external contribution history;
- propose a per-repository action.

Apply AGPL plus `NOTICE` to another repository only after explicit approval for that repository.

## Third-Party Code

Third-party files, generated files, models, datasets, and dependencies keep their own license terms. Do not overwrite third-party notices. If a file is not project-owned, do not add this project copyright header unless ownership has been confirmed.
