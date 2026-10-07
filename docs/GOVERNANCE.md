# Maintenance and repository governance

## Ownership and scope

[@ddtdanilo](https://github.com/ddtdanilo) maintains this independent community fork.
The purpose is to preserve tooling for existing Pycom modules, beginning with a
qualified local-package updater and native macOS support. It does not speak for
Pycom, provide vendor service guarantees, or promise support SLAs.

Repository-wide [CODEOWNERS](../.github/CODEOWNERS) requests maintainer review.
Contributors retain their copyright; no CLA or copyright transfer is required for
current documentation. [LICENSE.md](../LICENSE.md) defines the license boundaries.

## Stable branch policy

The default branch is `main`. Intended GitHub enforcement:

| Control | Policy |
| --- | --- |
| Pull requests | Required before merging |
| Independent approvals | At least one; last reviewable push needs approval by another person |
| Stale approvals | Dismissed after new changes |
| Required status | `repository-checks`; branch must be up to date |
| Unresolved conversations | Block merge |
| History | Linear; squash merge only |
| Force pushes / deletion | Disabled on `main` |
| Administrator exemption | Disabled |
| Code owner review | Review routing exists; not an additional mandatory approval |

The exact deployed state belongs to GitHub. Inspect Settings → Branches → `main`
or the REST branch-protection endpoint to verify it. Documentation alone does not
enforce a rule. The initial repository foundation is integrated before enabling
these controls; subsequent changes follow them.

With one maintainer, a maintainer-authored PR still needs another eligible reviewer.
The owner can review contributions from others but cannot approve their own change.
An emergency policy change must be deliberate and publicly documented afterward;
there is no automated bypass or CI workflow that pushes to `main`.

Independent approvals must come from eligible reviewers with write access. No
additional human reviewer has been designated during this bootstrap. Protection
is still enabled; maintainer-authored PRs wait until such a reviewer is available.
Contributors do not receive write access merely by submitting a PR.

For stale PRs, ask the author to update/rebase their branch. A maintainer who pushes
the update cannot approve that most recent push; another eligible reviewer is then
needed. Avoid using **Update branch** on a PR you intend to approve yourself.

Squash-only merging and the PR title as the default squash-commit title are
repository merge settings, separate from branch protection. PR title edits must
rerun CI so a corrected title can satisfy the required check.

## Decisions and change review

Small documentation corrections use focused PRs. Source imports, license choices,
protocol replacement, protection handling, and GUI technology
need an issue/ADR with alternatives, evidence, consequences, and a revisit trigger.
Only qualify support claims with traceable validation records.

Maintainers may request changes or decline work that expands scope prematurely,
obscures licensing, leaks secrets, or lacks necessary verification. Review is based
on the contribution, not donations or affiliation.

## Releases and maintenance continuity

No community updater release or supported runtime version exists yet. Original
tags/installers are historical upstream artifacts. The plan proposes `community-v`
tags and separate community release notes to avoid confusion.

Before a release, define its supported-version window and publish tested module,
host, driver, and operation boundaries. Record known limitations and recovery
instructions. Do not attach compatibility promises to donations.

If maintenance capacity declines, publish the affected scope, archival/deprecation
intent, and contributor handover options. Security and conduct reports follow
[SECURITY.md](../SECURITY.md) and [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md).
