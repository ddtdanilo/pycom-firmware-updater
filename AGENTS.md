# Repository instructions

## Current state and scope

- This is an independent personal community fork with docs, tooling, and redacted
  installer-reference research; no runnable community updater exists.
- The intended product is a native Apple Silicon desktop GUI; CLI work is supporting
  infrastructure. Intel/universal2 support is a qualified transition target.
- Write repository content in English. Preserve honest status and support boundaries.
- Read README.md, CONTRIBUTING.md, LICENSE.md, and the maintenance plan before changes.
- Do not import engine source, firmware, or binaries without the documented M0
  provenance/license decision. Do not edit inherited historical documentation.
- ADR 0001 records the maintainer-requested reference research exception. Recovered
  `.txt` files have unresolved rights, are not MIT, and must not become runtime imports.

## Collaboration and verification

- Work on a short-lived branch and open a PR to this fork's `main`.
- Follow CONTRIBUTING.md and docs/GOVERNANCE.md; never bypass protection automatically.
- Run `npm ci`, `npm run check`, and `git diff --check` for documentation/tooling changes.
- Static-inspection changes require synthetic failure/redaction/non-execution tests.
  Never execute recovered code or publish raw credentials/intermediates.
- Keep action references pinned, tokens minimal, and dependency lockfiles current.
- Add meaningful runtime checks when runtime code exists; repository CI is not
  hardware, architecture, flashing, signing, or notarization evidence.
- Keep README, support matrix, plan, and validation evidence consistent.
- Never publish secrets, device backups, credentials, or raw private logs.
- Do not connect to, reset, erase, or flash a physical device without explicit authorization.
- Use AI reviews as assistance; they do not replace required independent approval.

## Attribution and status

- Preserve upstream rights and distinguish future work from implemented behavior.
- Source claims use immutable references. Do not claim a release or compatibility
  before its qualified evidence exists.
- [Funding](https://buymeacoffee.com/ddtdanilo) is optional.
