# Repository instructions

## Current state and scope

- This is an independent personal community fork with documentation/tooling only.
- Write repository content in English. Preserve honest status and support boundaries.
- Read README.md, CONTRIBUTING.md, LICENSE.md, and the maintenance plan before changes.
- Do not import engine source, firmware, or binaries without the documented M0
  provenance/license decision. Do not edit inherited historical documentation.

## Collaboration and verification

- Work on a short-lived branch and open a PR to this fork's `main`.
- Follow CONTRIBUTING.md and docs/GOVERNANCE.md; never bypass protection automatically.
- Run `npm ci`, `npm run check`, and `git diff --check` for documentation/tooling changes.
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
