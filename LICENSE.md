# Licensing scope

## New community work

New original files authored for this community fork, including the current README,
plans, policies, templates, and repository-check tooling, are licensed under the
[MIT License](LICENSES/MIT.txt). Copyright © 2026 Danilo and community contributors.

Contributions to these files are made under the same license. No CLA or copyright
assignment is required. Contributors must have the right to contribute their work.

## Inherited material and external artifacts

| Material | Applicable status |
| --- | --- |
| `docs/UPSTREAM_README.md` and root `CHANGELOG.md` | Inherited Pycom documentation; no license file was published in the original updater repository. Original rights are retained; this fork does not relicense it. |
| Historical upstream commits and tags | Retain their original rights and notices. |
| Pycom installers and firmware | Not included in the new community work; no redistribution rights are asserted here. |
| Candidate engine in a separate repository | Not imported; file-specific GPL and Pycom terms require review. |
| Third-party dependencies and their license texts | Retain their own licenses; see package metadata and lockfile. |
| Names and trademarks | Retain their owners' rights; no endorsement is implied. |

The MIT grant applies only to new community-authored work, not the entire upstream
history or external artifacts. The license of a future runtime must be selected
after its dependencies and reused source are reviewed. See
[source provenance](docs/SOURCE_PROVENANCE.md) and milestone M0 in the
[maintenance plan](docs/MAINTENANCE_PLAN.md).

A future binary that combines GPL-licensed components must satisfy the applicable
terms for that combination, including corresponding-source obligations. MIT on
individual community files does not make a combined GPL application MIT-licensed.
