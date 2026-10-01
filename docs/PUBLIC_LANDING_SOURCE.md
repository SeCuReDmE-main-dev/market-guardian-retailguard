# Public landing source

`web/landing/` is the source for the existing public preview at
<https://market-guardian.securedme.ca/>. Its eight original files were recovered
on 2026-09-30 from the maintainer's earlier local checkout after comparing every
file byte-for-byte with the published HTTPS origin. The earlier checkout and
its unrelated edits were preserved. This recovery does not replace the backend
or turn the synthetic review preview into a production service.

The original source checkout was at commit
`20b7b3674cf1e5d13ef0eeb317c1bf4fded347de`. Public browser setup additions are
distributed by the website's `tools/sync_public_browser_setup.py`: the
HTML-in-Canvas trial is detected without requiring it, and public analytics load
only after an explicit choice. No synthetic evidence, review text or learner
inputs are included in analytics.

Use a local static server to inspect this directory. Deployment must use the
governed Education Controller, Settings mutation gate, and exact plan-bound
confirmation. Do not run historical direct-credential deployment scripts.
