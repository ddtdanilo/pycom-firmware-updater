# Pycom Firmware Updater — Community Maintenance

[![Repository checks](https://github.com/ddtdanilo/pycom-firmware-updater/actions/workflows/repository-checks.yml/badge.svg)](https://github.com/ddtdanilo/pycom-firmware-updater/actions/workflows/repository-checks.yml)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy_Me_a_Coffee-Support_this_project-FFDD00?logo=buymeacoffee&logoColor=000000)](https://buymeacoffee.com/ddtdanilo)

Keep existing Pycom hardware usable through a native Apple Silicon graphical updater.

This community-maintained fork aims to preserve a practical way to inspect, back up,
recover, and update Pycom's ESP32-based modules through a maintained **desktop GUI**.
The main reason is macOS ending the Intel/Rosetta compatibility path: existing
hardware should not become unusable because its updater depends on an obsolete
host architecture. Native Apple Silicon is the primary target; a **macOS universal2
application** can also serve Intel Macs during the transition, once qualified.

**Current status: installer recovery, planning, and repository foundations.**
Redacted reference code, disassembly, and reproducible static-analysis tooling are
available. This fork has no runnable GUI, imported flashing engine, community
binary, or verified hardware support yet. The roadmap describes future work.

This is an independent community effort, maintained by [Danilo](https://github.com/ddtdanilo).
It is not an official Pycom release and is not affiliated with or endorsed by Pycom.

## Start here

| You want to… | Read |
| --- | --- |
| Understand the implementation sequence and release gates | [Maintenance plan](docs/MAINTENANCE_PLAN.md) |
| Understand the proposed design | [Architecture](docs/ARCHITECTURE.md) |
| Inspect recovered code and the route to a native GUI | [Recovery findings](docs/RECOVERY_FINDINGS.md) · [Reference snapshot](research/installer-v1.0.3/README.md) |
| Read the recovered classic graphical wizard | [Classic GUI 1.16.6 recovery](research/classic-gui-1.16.6/README.md) |
| Check the planned modules, platforms, and validation requirements | [Support matrix](docs/SUPPORT_MATRIX.md) |
| Check the source investigation and what can be reused | [Source provenance](docs/SOURCE_PROVENANCE.md) |
| Inspect the plan review and repository checks | [Review record](docs/PLAN_REVIEW.md) · [Tooling](docs/TOOLING.md) |
| Help with code, documentation, or hardware testing | [Contributing](CONTRIBUTING.md) |
| Report a security concern privately | [Security policy](SECURITY.md) |

## Why this fork exists

The [original updater repository](https://github.com/pycom/pycom-firmware-updater)
was archived in September 2024. Its published Git history contains documentation
and links to installers, rather than the source of the desktop application.
A fork of that repository therefore cannot simply rebuild the original GUI for ARM.

[Apple's published Rosetta transition](https://developer.apple.com/news/?id=w5ngl9k2)
makes native Apple Silicon support necessary for continued availability of
Intel-only applications. The [installer investigation](docs/RECOVERY_FINDINGS.md)
confirmed that the historical macOS asset contains an x86_64 Python service with
a Qt tray icon and local WebSocket interface. It yielded partial recovered code,
but no complete graphical frontend in that package. A **separate public 1.16.6
desktop application** was then recovered: its Python 2.7/PyQt4 wizard and ten
supporting modules are available as [reference text](research/classic-gui-1.16.6/README.md).
The intended result is a standalone GUI that
works with local packages and a qualified core, without relying on Rosetta.

Pycom did publish a Python command-line engine separately, under
[`esp32/tools/fw_updater` in `pycom-micropython-sigfox`](https://github.com/pycom/pycom-micropython-sigfox/tree/a37510c092bcec00671c924accb97dcdfa2f4b5d/esp32/tools/fw_updater).
That engine is the candidate foundation for a maintained CLI and a new desktop
interface. Importing it requires an explicit provenance and license review;
modernizing it requires compatibility tests, not just repackaging.

## Intended scope

- Prioritize WiPy 2/3, LoPy, LoPy4, SiPy, FiPy, and GPy as candidate modules.
- Support local firmware packages without requiring a vendor cloud account.
- Make device identification, backup, and preflight checks precede flashing.
- Preserve device configuration, credentials, and filesystem data where readable
  and verified, unless the operator explicitly chooses an operation that changes them.
- Provide useful diagnostics, an accessible desktop UI, and an optional scriptable CLI.
- Ship independently verified ARM and Intel compatibility before claiming
  universal support.

The original WiPy 1, generic ESP32 boards, expansion-board firmware, and LTE modem
firmware are outside the initial target. Radio certifications, network subscriptions,
and vendor cloud services are also outside the updater's control. See the
[support matrix](docs/SUPPORT_MATRIX.md) for the exact boundaries.

## What is available today

| Item | Status |
| --- | --- |
| Community mission, technical plan, and contribution guidance | Available |
| Historical installer inventory, redacted references, and static inspection tool | Available; partial recovery, not runtime code |
| Classic desktop wizard and supporting modules | Recovered as research references; no maintained GUI build yet |
| Documentation lint and repository consistency checks | Configured in CI |
| Public candidate CLI source in the separate Pycom firmware repository | Identified; not imported |
| New CLI or desktop application in this fork | Not implemented |
| ARM, Intel, or universal2 community build | Not built or tested |
| Device recovery, data preservation, or flashing verification | Not tested |
| Signed and notarized community installer | Not available |

There is no community installation command yet. Upstream release assets and tags
are historical artifacts, not releases produced or validated by this fork.
The [original README](docs/UPSTREAM_README.md) is preserved for provenance; its
installation instructions are historical and are not current community guidance.

## Development and contributions

For the current documentation and research phase:

```sh
git clone https://github.com/ddtdanilo/pycom-firmware-updater.git
cd pycom-firmware-updater
npm ci
npm run check
```

These commands require Node.js 22 or newer and Python 3.10 or newer. Node.js is
used for documentation checks; it is not a commitment to a JavaScript application.
They do not install an updater or access a connected device. The documentation's
Python requirement is separate from the future runtime support policy.

Hardware owners can help most by documenting their module revision, expansion
board, operating system, USB bridge, and firmware package provenance. Never attach
raw device backups, activation tokens, or credentials to public issues.
Start with [CONTRIBUTING.md](CONTRIBUTING.md), and follow the
[Code of Conduct](CODE_OF_CONDUCT.md).

## Roadmap

1. Resolve provenance, redistribution terms, and representative test fixtures.
2. Build a desktop GUI shell with a simulated backend while qualifying the core.
3. Integrate qualified diagnostics, backup, preservation, flashing, and recovery.
4. Validate the complete GUI on native Apple Silicon; then qualify universal2.
5. Sign, notarize, and publish the application with release evidence.
6. Expand platform and module coverage as reproducible results become available.

The optional CLI supports core testing and automation; a CLI alone does not fulfill
the graphical application goal. The [full maintenance plan](docs/MAINTENANCE_PLAN.md) defines dependencies,
deliverables, acceptance criteria, open decisions, and release blockers for every
milestone. No release date or untested compatibility is promised.

## Licensing and attribution

New community-authored files are provided under the MIT license; the inherited
upstream README and changelog retain their original, unresolved licensing status.
The redacted installer-derived references retain unresolved original rights and
are excluded from MIT; they are not a license-cleared runtime import. No license
is granted here over Pycom's installers, firmware, trademarks, or separately
published code. The candidate engine declares GPL and Pycom-specific
terms, which must be resolved before it is imported or redistributed.
See [LICENSE.md](LICENSE.md) and [source provenance](docs/SOURCE_PROVENANCE.md).

Pycom and the original contributors deserve credit for the hardware, firmware,
and published tooling on which this maintenance effort builds.

## Support the maintenance effort

If this project helps keep your hardware in service, you can support the work:

**[Buy me a coffee](https://buymeacoffee.com/ddtdanilo)** ☕

Donations are optional. Hardware reports, documentation fixes, and code reviews
are equally welcome. A donation does not purchase support priority, a delivery
date, or a compatibility guarantee.
