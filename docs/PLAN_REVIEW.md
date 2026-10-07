# Technical plan review record

## Scope and reviewer

On 2026-10-06, the maintainer requested plan enrichment using **Claude Opus 5.5**
with **medium effort**. A noninteractive Claude Code 2.1.292 review was run with
`--model claude-opus-5-5 --effort medium`. The successful result reported
`claude-opus-5-5` in model usage; no fallback model was used.

The reviewer received the README, maintenance plan, architecture, support matrix,
source provenance, license scope, contribution/governance rules, security policy,
and conduct policy. Tools were disabled. It critiqued the supplied documentation,
not live GitHub state, runtime behavior, hardware, or legal clearance.

## Improvements incorporated

- Split release delivery into a useful read-only CLI, qualified flashing CLI,
  and universal2 desktop track instead of requiring a GUI before useful tooling.
- Decomposed source/license decisions by transport, package semantics, and PIC
  protocol, with separate firmware-availability and rights-holder questions.
- Added an explicit recoverability/data model, including unique flash content,
  peripheral firmware, one-time state, and physical failures.
- Added DTR/RTS and macOS call-out guidance, qualified by pyserial's documented
  warning that opening a port may still cause driver/OS glitches.
- Added controlled hardware failure-injection, baseline backups, and qualification
  reassessment/withdrawal rules.
- Strengthened binary audits, signing/notarization evidence, release environments,
  tag protection planning, and the boundary around self-hosted hardware runners.
- Clarified strict-review consequences for a sole maintainer and stale-PR updates.
- Added CI triggering on PR title edits and separated squash settings from protection.
- Linked the observed 4 MB parser detail to a pinned source line range and
  documented the organization-search method.

## Findings independently checked or bounded

The review raised possible missing-lockfile/default-branch/check-name problems;
those required live verification because the reviewer did not have the full
tooling or GitHub state. The actual lockfile is committed, GitHub's default is
`main`, and the workflow job is named `repository-checks` without path filters.

The reviewer suggested legal interpretations and technical options. This plan
records them as questions or candidates, not decisions about redistribution,
eFuse behavior, credential location, or current-device support.

Repository checks and dependency auditing are separate evidence. This review is
not an independent human PR approval, a hardware qualification, or proof that
an application has been built. See [the plan](MAINTENANCE_PLAN.md) and
[support matrix](SUPPORT_MATRIX.md) for the remaining gates.

## Installer and classic GUI recovery review

Two additional tool-free reviews used `claude-opus-5-5 --effort medium` on
2026-10-06. Both results confirmed that exact model in usage. The supplied scope
included the static inspector, synthetic tests, publication/provenance checker,
GUI recovery findings, source boundaries, and reproduction documentation. The
classic extension was included in the second recovery review.

Corrections incorporated: cumulative expansion limits, exact credential-constant
replacement, PEM/userinfo redaction and scanning, valid unresolved-rights notices,
case-collision rejection, normalized paths/headers, single-read input identity,
captured decoder versions, protected analysis fields during publication, preserved
literal whitespace, an explicit grammar-check script/report, and separate classic
wizard/service provenance. The original credential values were checked locally
against tracked text without disclosing them.

The reviews also raised broader detector/decoder limitations. The tools are scoped
static research decoders for identified historical inputs, not generic secret
certification or a hardened execution sandbox. AI review did not execute the
application, inspect hardware, clear licenses, or provide human PR approval.
