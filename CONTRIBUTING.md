# Contributing

Thank you for helping keep existing Pycom modules usable. Documentation, source
investigation, reviews, and careful hardware reports all matter. Read the
[README](README.md), [plan](docs/MAINTENANCE_PLAN.md), and
[Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## Current phase

This repository contains a plan, tooling, and redacted installer-reference research,
not a runnable updater. The end product is a native Apple Silicon desktop GUI;
the CLI is supporting infrastructure, not a replacement for that deliverable.
Do not run unimplemented commands or present planned features as available.
Discuss runtime source imports and major design changes before implementing them;
the provenance and license gate must be resolved first.

The [reference recovery decision](docs/decisions/0001-installer-reference-recovery.md)
allows the explicitly requested historical research snapshot. It does not clear
runtime reuse or grant a license over the recovered text. Keep raw intermediates
outside the checkout and review any research export for secrets and rights scope.

## Where to contribute

- Use a bug report for a reproducible documentation/tooling defect.
- Use a feature proposal for scope or architecture changes, with alternatives.
- Use a hardware report for existing results you are authorized to share. Providing
  a report does not require performing a new flash operation.
- Use [private vulnerability reporting](https://github.com/ddtdanilo/pycom-firmware-updater/security/advisories/new)
  for security issues; follow [SECURITY.md](SECURITY.md).
- Keep issues and PRs in English so the maintenance effort is accessible globally.

Never submit credentials, activation tokens, full device identifiers, proprietary
firmware without permission, private backups, or raw secret-bearing logs.

## Branch and pull-request rules

`main` is the stable default branch. Work on short-lived branches such as
`docs/<topic>`, `feat/<topic>`, or `fix/<topic>`, and submit a pull request into
this personal fork's `main`. Do not send this fork's maintenance PRs to upstream.

The merge policy is documented in [governance](docs/GOVERNANCE.md) and enforced by
GitHub settings once enabled; the live settings are authoritative:

1. Every change to `main` goes through a pull request.
2. The `repository-checks` status must pass against the current base branch.
3. At least one independent approval is required, including approval of the most
   recent reviewable push by someone other than its author. Stale approvals dismiss.
4. Resolve review conversations before merging.
5. Squash merge with a meaningful Conventional Commit title; `main` stays linear.
6. Force pushes and branch deletion are blocked on `main`, including for admins.

A sole maintainer cannot independently approve their own PR. Such a PR needs
another eligible reviewer; do not weaken protections as a routine workaround.
CODEOWNERS routes review to the maintainer but does not replace independent review.

Keep a PR focused. Describe the concrete problem, resulting behavior, evidence,
validation performed, and limitations. Link related issues using `Closes #123`
only when the change actually resolves them.

## Local checks

Requirements: Node.js 22+ and Python 3.10+. No hardware is needed for these checks.
See [repository tooling](docs/TOOLING.md) for their scope and limitations.

```sh
git clone https://github.com/ddtdanilo/pycom-firmware-updater.git
cd pycom-firmware-updater
git switch -c docs/your-topic
npm ci
npm run check
git diff --check
```

Commit examples: `docs: clarify recovery scope`, `fix: validate relative links`,
`feat: add package inspection`. PR titles use `type: description` or
`type(scope): description`, without a trailing period. CI checks this convention.

Commit dependency lockfiles whenever dependency manifests change. Do not add
downloaded binaries, firmware packages, local secrets, generated build output, or
device backups. Use synthetic fixtures or small redistributable samples once
runtime tests exist.

## Documentation and support claims

- Keep project prose in English and use relative links within the repository.
- Cite immutable upstream source revisions for implementation claims.
- Mark proposals, open decisions, and validation limitations explicitly.
- Keep README, plan, and support matrix consistent when capabilities change.
- A build passing is not physical-device verification. A port opening is not a
  successful update. Never advertise unsupported combinations.
- Preserve the inherited `docs/UPSTREAM_README.md` and `CHANGELOG.md`; community
  release notes will use a separate changelog.

## Future code and hardware changes

Before runtime work, resolve M0 licensing and record the implementation ADR.
Future parser/transport changes need meaningful fixtures and failure-path tests;
destructive behavior needs explicit preservation intent, protected-range rules,
and physical-device evidence before release.

Hardware reports identify host OS/architecture, module/expansion revision, USB
bridge/driver, tool/package hashes, operation intent, and redacted results.
Testing is voluntary and requires hardware you are authorized to modify. Do not
claim a successful recovery or preserved credentials without verifying it.

## License and review responsibility

New community files use MIT as scoped in [LICENSE.md](LICENSE.md). Retain original
notices and identify third-party terms; never assume the repository's root license
covers separate Pycom source or firmware. No CLA is currently required.

AI assistance is welcome, but the contributor remains responsible for correctness,
source rights, secrets, tests, and support claims. State material assistance in the
PR when it helps reviewers understand the work. An AI review does not satisfy
GitHub's required independent human approval.
