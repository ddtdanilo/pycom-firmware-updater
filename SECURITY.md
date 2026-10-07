# Security policy

## Supported versions

There are no community runtime releases to support yet. This fork currently
contains documentation and repository-check tooling. Historical Pycom installers
and externally referenced firmware have not been validated by this fork.

Report problems in this fork's workflows, dependencies, documentation, or future
runtime through the channel below. For an external Pycom artifact, identify its
origin so maintainers can determine which project owns the issue.

## Private reporting

Use GitHub's **Report a vulnerability** form:

[Submit a private report](https://github.com/ddtdanilo/pycom-firmware-updater/security/advisories/new).

Include the affected file/version, impact, reproduction steps, environment, and
a minimal non-secret example. Never publish credentials, device backups, private
keys, activation tokens, or exploit details in a public issue.

The maintainer reviews reports on a best-effort basis; no response deadline or
security support SLA is promised. Coordinate public disclosure after impact and
mitigation are understood. If the form is unavailable, open a public issue asking
for a private reporting channel without including the vulnerability details.

## Future runtime security requirements

Untrusted package validation, protected flash regions, explicit destructive consent,
private backup handling, log redaction, dependency audits, release signing, and
notarization are release gates in the [maintenance plan](docs/MAINTENANCE_PLAN.md).
They are not implemented runtime protections today.

PR checks do not receive release/signing secrets. Release credentials must be
isolated from untrusted PR code. Avoid `pull_request_target` execution of contributor
code and use minimal workflow permissions and immutable action references.
