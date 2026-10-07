# Community maintenance plan

**Status:** installer-reference research and proposed implementation plan;
no runnable community updater exists in this fork.
**Planning baseline:** 2026-10-06.
**Owner:** [@ddtdanilo](https://github.com/ddtdanilo).

## Mission and measurable outcome

Maintain a documented, testable path for keeping existing Pycom ESP32 modules
usable as macOS ends the Intel/Rosetta compatibility path. Preserve recoverability
and user data while delivering a maintained **desktop GUI**, supported by a shared
core and an optional CLI. A CLI-only result does not fulfill the product objective.

The first application release objective is a local-package graphical updater for
explicitly validated module/expansion-board combinations on native Apple Silicon,
without Rosetta. A subsequent universal2
release must run natively on ARM and Intel, without Rosetta. Windows and Linux
remain later targets until their own evidence is available.

Success means that a documented physical device can be identified, backed up,
updated from a provenance-recorded firmware package, verified, and returned to a
working boot state. A build or serial-port listing alone is insufficient.

## Evidence baseline and constraints

- The original updater repository publishes documentation and installers, not
  desktop application source. This fork preserves its ancestry.
- Static installer recovery yields a Python 3.9 x86_64 service, WebSocket actions,
  and Qt tray code, with 24 candidate modules disassembled and 23 partial source
  previews. A full GUI was not found in that asset. See [findings](RECOVERY_FINDINGS.md).
- A separate public desktop `1.16.6` DMG provides Python 2.7/PyQt4 GUI recovery:
  eleven candidate GUI/core modules, including the wizard, query/fetch/upgrade
  workers, and configuration. Its previews pass Python 2 syntax checks, not
  semantic, hardware, or modern-host qualification.
- Recovered references have unresolved rights and are not runtime imports. Automatic
  previews contain omissions/mistranslations; disassembly is research evidence.
- A separate candidate Python engine contains `updater.py`, `esptool.py`, and
  `pypic.py`. Pin its exact revision before any import.
- Its CLI exposes flashing, backup/restore, identifiers, configuration, and reset
  options. Their existence in source is not proof of current compatibility.
- Package handling includes legacy `script`/`script2` and flash-size-specific
  metadata. A generic esptool invocation is not an equivalent replacement.
- GPL declarations reference Pycom-specific terms; MicroPython's root MIT license
  does not settle the updater's license.
- Vendor endpoints, firmware availability, USB drivers, and host dependencies need
  fresh verification. Prioritize local/offline workflows.

See [source provenance](SOURCE_PROVENANCE.md), [architecture](ARCHITECTURE.md), and
the [support matrix](SUPPORT_MATRIX.md).

## Scope and operating principles

Initial candidates are WiPy 2/3, LoPy, LoPy4, SiPy, FiPy, and GPy. The initial
workflow accepts authorized local firmware, exposes read-only diagnostics,
requires explicit device selection, and provides backup, controlled update, and
post-write verification. Implement the CLI before the GUI.

Defer WiPy 1, generic ESP32 targets, expansion-board MCU firmware, LTE modem
firmware, OTA, online catalogs, cloud login, telemetry, and manufacturing tools.
Preservation does not promise to restore unavailable network or cloud services.

Future implementations must follow these rules:

1. Listing ports is read-only and never toggles reset lines.
2. Display the device, package, partition writes, preservation boundaries, and
   erase intent before writing; CLI and GUI share one operation plan.
3. Preserve filesystem, NVS, configuration, and device-specific identifiers by
   default where readable. Refuse a preservation claim for unreadable regions.
4. Require explicit consent for destructive effects and fail closed when identity,
   flash capacity, package compatibility, or device protection is uncertain.
5. Never burn eFuses or change encryption/secure-boot provisioning in an ordinary
   update. Initially reject protected-device workflows that lack qualification.
6. Keep backups, secrets, and raw serial logs out of source control and public reports.
7. Treat cancellation, cable removal, power loss, and partial writes as recovery
   states. Do not imply that an interrupted write was undone.
8. A validated local-package operation requires no network connection.

## Recoverability model

Recovery depends on which state was changed and whether the qualified bootloader
path is still reachable. Do not use a successful firmware rewrite as proof that
device-unique data was recovered.

| State class | Examples to inventory | Recovery requirement |
| --- | --- | --- |
| Reproducible flash content | Bootloader image, partitions, application | Compatible authorized package and reachable programming path |
| Device-unique flash content | Configuration, flash-resident credentials, filesystem | Verified backup of that exact device and a qualified restore path |
| One-time programmable state | Secure-boot/encryption-related eFuses | Not rewritable; ordinary updater never changes it |
| Peripheral firmware | Expansion-board PIC, LTE modem | Separate tooling and recovery procedure; excluded initially |
| Physical fault | Power, cable, voltage, damaged hardware | Diagnose the physical setup; software recovery is not assured |

M0/M3 must identify which credentials and identifiers are flash-resident,
eFuse-derived, or peripheral-specific for each target. Until established, treat
non-firmware regions as device-unique. A full-flash backup is not a backup of every
peripheral or one-time-programmable state.

## Incremental release tracks

The GUI remains the final product. R0/R1 are core qualification and optional
intermediate tooling tracks. Start an original GUI shell with a simulated backend
in parallel; do not postpone all interface work until a CLI release exists.

| Track | Useful deliverable | Component gate | Qualification gate |
| --- | --- | --- | --- |
| R0 | Read-only CLI: discovery, identity, protection summary, backup/verification | Cleared upstream transport; no unresolved Pycom code | M1 and M3 read paths |
| R1 | Package inspection/dry run, then qualified CLI update/restore | Cleared package/PIC semantics as used | M2 and M4 |
| R2 | Native/universal2 desktop application | R1 shared core and cleared GUI dependencies | M5–M7 desktop gates |

R0 can evaluate maintained Espressif esptool for reading/identity without importing
the Pycom package/PIC code. Its licenses, exact version, silicon compatibility, and
required manual bootloader entry still need verification. Do not silently assume
it replaces the candidate engine for package flashing.

A qualified R0/R1 may be distributed as a versioned Python package before the GUI
exists, with locked inputs, checksums, notices, corresponding source where required,
and explicit host/device evidence. Standalone native macOS artifacts still need
their applicable signing/distribution gates. No track exists today.

M7 controls apply per artifact: the Python-only CLI need not wait for a GUI, but
a desktop universal2 claim requires both native host and GUI qualification.

## M0 — Provenance and licensing

**Dependencies:** none. **Status:** open; the initial inventory is documented.

### Deliverables

- Per-file import manifest: upstream URL/revision, SHA-256, notices, modifications,
  license declaration, and redistribution basis.
- Resolve the exact terms of installer-derived components before any runtime reuse.
  Preserve the [research decision](decisions/0001-installer-reference-recovery.md),
  module provenance, redactions, and recovery limitations. Do not assume the missing
  installer license or service terms grant source redistribution rights.
- Inventory the separate GUI/frontend, if obtainable, independently of the recovered
  service. The classic wizard is now available as unresolved-rights reference text;
  record per-component reuse decisions before a port or use it only for a reviewed
  reconstruction process. A local desktop UI must be qualified independently.
- Review of updater/PIC Pycom-specific terms and esptool GPL obligations. Select
  the application license after deciding how the engine will be reused.
- Decide reuse per component: ESP32 bootloader transport, Pycom package semantics,
  and PIC reset protocol. A blocked import must not prevent unrelated original
  parser/UI work or a separately cleared read-only transport track.
- Identify the relevant rights holders and a documented permission route where
  needed. Any independent reimplementation must have a recorded, reviewed process;
  do not copy restricted source into a purported independent implementation.
- Inventory obtainable firmware using filename, version, size, SHA-256, original
  URL, and observation date. Publish metadata only unless binary redistribution
  is authorized. Record source-build options and any binary-blob limitations.
- Consider archival of legally redistributable sources and record immutable
  archival identifiers when obtained; upstream hosting is not a permanence guarantee.
- Authorized fixture inventory; use synthetic packages where real firmware cannot
  be redistributed. Do not import proprietary installers as application source.
- Upstream attribution, historical tag policy, security reporting, and maintainership.

### Acceptance criteria

Every imported/distributed artifact has a documented license basis and provenance.
Unresolved artifacts are excluded. If reuse is blocked, record a decision to seek
permission or pursue an independently implemented compatible tool. New MIT
documentation never relicenses inherited or separately imported code.

## M1 — Maintained Python core

**Dependencies:** M0 for source import. **Status:** not started.

### Deliverables

- `pyproject.toml`, `src/` layout, isolated installation, CLI entry point, explicit
  Python support policy, dependency locks, and reproducible build inputs.
- Evaluate Python 3.12 as an initial baseline; record the choice using dependency
  availability and lifecycle evidence rather than treating it as settled.
- Isolated Pycom serial/PIC adapter retaining required protocol behavior; compare
  vendored esptool with alternatives before replacing it.
- Audit Python 2 compatibility, bytes/text conversions, integer arithmetic,
  exceptions, serial deadlines, retries, resource cleanup, and platform assumptions.
- Separate pure package/configuration logic from hardware and host-specific code.
- Typed operation plans, stable error categories, structured progress, and logs.
- Runtime lint/type checks, pytest, meaningful coverage, dependency audit, and
  secret scanning once runtime code exists.

### Acceptance criteria

A clean checkout installs in an isolated environment without a device. Importing
the core never opens a serial port or contacts a service. Help/version and package
inspection work offline. The selected Python matrix passes the same checks.

## M2 — Package validation and compatibility model

**Dependencies:** M1. **Status:** not started.

### Deliverables

- Model family, revision, flash size, expansion board, reset strategy, radio
  variant, protection state, and partition layout separately.
- Synthetic fixtures for `script`, `script2`, 4 MB/8 MB metadata, missing/duplicate
  members, malformed JSON, invalid instructions, overlaps, and wrong targets.
- Regression tests for the [candidate 4 MB parsing path](https://github.com/pycom/pycom-micropython-sigfox/blob/a37510c092bcec00671c924accb97dcdfa2f4b5d/esp32/tools/fw_updater/updater.py#L168-L177)
  (`json.load` receives decoded text) and broad fallback handling before changing behavior.
- Validate member names/types/count, decompressed size, instruction count, allowed
  commands, alignment, range bounds, reserved regions, and compatible layouts.
  Reject traversal, symlinks, duplicates, decompression bombs, and unknown commands.
- Read members without extraction where possible; otherwise use an explicitly
  constrained temporary directory and extraction filters.
- An immutable complete operation plan and deterministic dry-run output.
- A firmware trust policy distinguishing content hashes from publisher authenticity.

### Acceptance criteria

Known valid formats yield repeatable plans. Unsupported inputs fail before device
I/O. Unknown metadata never triggers a permissive fallback. A dry run identifies
exact writes/erases and preservation boundaries without contacting hardware.

## M3 — Diagnostics and verified backups

**Dependencies:** M1 for read paths; M2 for package-aware restore/preservation paths.
**Status:** not started.

### Deliverables

- Passive port enumeration and explicit selection when multiple devices exist.
- Enumerate through OS/list-port APIs without opening ports. For probing, construct
  pyserial with `port=None`, configure DTR/RTS explicitly, then open using the
  qualified reset sequence. OS/driver glitches may still toggle lines; validate
  this physically and do not promise passive behavior after opening.
- Prefer macOS `/dev/cu.*` call-out ports, and record expansion PIC firmware
  version where readable because handshake behavior may depend on it.
- Separate, documented FTDI/PIC/manual-bootloader strategies. Confirm USB bridge
  and driver behavior without bundling unverified or unlicensed drivers.
- Bounded identity/flash probes, conservative baud negotiation, busy-port and
  disconnect errors, and explicit disclosure that bootloader entry interrupts
  a running device even when the subsequent operation only reads.
- Local backup manifests identifying device/layout, offsets/lengths, checksums,
  firmware/tool version, and incomplete/unreadable regions.
- Atomic private backup files; permissions, disk-full, truncation, and checksum tests.
- Restore compatibility checks; no casual cross-device restore of credentials,
  identifiers, or incompatible layouts.
- Redacted diagnostics without raw backups, full MAC addresses, activation tokens,
  Wi-Fi credentials, or Sigfox PACs/keys.

### Acceptance criteria

Repeated reads of a quiescent device have stable hashes. Corrupt backups fail
verification before restore is offered. Incomplete/protected backups are labeled
accurately. Entering programming mode requires informed operator agreement.

## M4 — Controlled flashing and recovery

**Dependencies:** M2–M3 and authorized test hardware. **Status:** not started.

### Deliverables

- Per-device locking and execution of one preflight-approved operation plan.
- Separate update, factory reset, partition restore, and expert recovery workflows.
  Preserve user/device-specific data by default; require explicit erase intent.
- Private local operation journal with completed ranges and verification outcomes.
- Bounded safe-point retries, programmed-block verification, partition checks,
  and final boot/REPL smoke checks where supported.
- Failure injection before/during erase, during write, before reboot, on disconnect,
  and at cancellation boundaries. Define safe and unsafe cancellation states.
- Designate authorized test units, verify their full-flash baseline backups before
  first destructive use, and retain device-unique data privately. Where available,
  use a controllable power/USB rig for repeatable failure injection. Distinguish
  physical power loss from simulated disconnects in every report.
- Device reidentification before recovery; no blind resume of an old offset/port.
- Restoration tests and independent configuration/filesystem preservation markers.
- Recovery guidance for bootloader entry, power/USB faults, wrong baud rate, and
  port contention.

### Acceptance criteria

At least one identified module/expansion-board combination passes an end-to-end
Apple Silicon qualification with a local package. Programmed ranges and post-boot
checks match the plan; preservation markers survive. Failure/recovery results are
reviewed. Protected-device, eFuse, modem, and expansion firmware paths stay disabled
unless independently qualified.

## M5 — Native macOS and universal2 builds

**Dependencies:** M4 for release qualification; build experiments may follow M1.
**Status:** not started.

### Deliverables

- ARM-only prototype, then an Intel build tested natively. Rosetta may assist
  diagnosis but does not prove native Intel USB/hardware interoperability.
- Minimum macOS version chosen from actual dependency and physical-device results.
- Universal2 Python and compatible native dependencies with PyInstaller's
  `--target-arch universal2`, if that packaging route is selected.
- Recursive audit of Mach-O executables, Python extensions, and transitive dylibs:
  architecture slices, deployment targets, linkage, and notices.
- Explicit ARM/Intel CI jobs and architecture assertions; verify runner labels
  when implementing them instead of assuming `macos-latest` is Intel.
- Never run untrusted public PR jobs on a hardware-connected or secret-bearing
  self-hosted machine. Keep physical qualification as an explicitly authorized,
  isolated process even if its results are later attached to a PR.
- Minimize compiled dependencies and evaluate a python.org universal2 interpreter.
  Inspect actual artifacts rather than assuming an installation source guarantees
  every dependency has both slices.
- Record `lipo -archs`, `vtool -show-build` or `otool -l`, and `otool -L` evidence
  for slices, deployment targets, and accidental host-specific library paths.
- Clean-host installation/startup without Python, Homebrew, or Rosetta. Exercise
  discovery, backup, flash, and verification on native ARM and Intel hardware.

Do not combine finished PyInstaller onefile executables with `lipo`: their embedded
archives do not become a working universal application. Resolve thin dependencies
at the library/wheel level, change toolkit, or distribute clearly labeled separate
native builds. Compare `onedir`/`onefile`; prefer an inspectable app bundle where
signing, troubleshooting, and startup behavior are clearer.

### Acceptance criteria

Every required bundled binary has the correct architecture support. The same
universal distribution passes both native host qualifications without a developer
environment. Missing slices, accidental Homebrew linkage, or absent hardware
evidence block a universal2 compatibility claim.

## M6 — Desktop interface

**Dependencies:** original simulated GUI work can begin alongside M0/M1; real
read paths require M3 and destructive workflows require M4.
**Status:** reconstruction requirements documented; application not implemented.

### Deliverables

- GUI toolkit ADR comparing PySide6/Qt, Tkinter, and SwiftUI: accessibility,
  licensing, universal dependencies, size, cross-platform cost, and maintenance.
- Standalone desktop GUI is the product acceptance target. Use recovered action
  names and component boundaries as reference, not automatic source imports.
- Local GUI assets and local-package updates work without Pybytes login, vendor
  certificate retrieval, hosts-file modifications, or a remote frontend.
- A simulated backend exercises empty/loading/error, cancellation, partial-write,
  and recovery screens before hardware integration. Simulation is visibly labeled
  and cannot invoke transport or qualify device behavior.
- Shared core validation/planning; no UI-only flashing rules or bypasses.
- Workflow: select device → inspect package → review backup/preservation →
  confirm operation → progress → verification or recovery result.
- Background serial workers, controlled cancellation, keyboard navigation,
  readable contrast, screen-reader labels, and honest progress states.
- Qualify the full workflow with macOS VoiceOver and Full Keyboard Access, including
  destructive confirmation, empty/loading/error screens, and partial-write states.
  Use WCAG2ICT as an accessibility assessment reference and document limitations.
- Ordinary-language target/package/erase explanations, local backup location,
  actionable errors, and redacted report export.
- Bounded logs and no cloud account, telemetry, or unrelated secret collection.

### Acceptance criteria

CLI/GUI fixture inputs produce the same plan/errors. A hardware owner can follow
the supported workflow and understand partial-write recovery. Each claimed native
host architecture passes startup and declared device workflows.

The initial native ARM application release must complete the supported GUI workflow
on a clean host without Rosetta. A CLI or tray/service-only port does not satisfy
M6. Intel results are required for a universal2 claim, not for the initial ARM-only
qualification; label architecture scope explicitly for each artifact.

## M7 — Release integrity and community operation

**Dependencies:** M0–M6 for a desktop release. **Status:** not started.

### Deliverables

- Community versioning/tags, initially proposed as `community-v`, without collisions
  with inherited tags. Keep original CHANGELOG.md historical and start a community
  changelog when actual releases begin.
- Separate unprivileged PR checks from a manually approved release workflow. Pin
  actions to full SHAs, restrict tokens, and keep secrets away from fork PRs.
- Apple Developer ID signing of nested code/app/installer, isolated temporary
  keychains, protected signing credentials, and cleanup.
- Record hardened-runtime, timestamp, and minimum-entitlement decisions. Notarize
  and staple the appropriate app/installer container; a standalone CLI is not
  itself a staplable distribution container.
- Notarization/stapling plus signature/Gatekeeper checks on clean hosts. Ad-hoc
  signing is not a signed/notarized public-distribution claim.
- Verify with `codesign`, `spctl`, and `stapler` as applicable, including a quarantined
  first launch and offline behavior after stapling. Record exact commands/results.
- Protect community release tags against replacement/deletion when releases start.
  Use a protected release environment and independent approval when a reviewer is
  available. Document the release actor and any maintainer-only bootstrap exception.
- Checksums, SBOM, corresponding source, notices, build recipe, artifact/source
  mapping, validation evidence, and limitations alongside each release.
- Evaluate verifiable build provenance attestations and PyPI Trusted Publishing
  for the relevant distribution track; keep upload credentials out of general CI.
- Rebuildability through pinned inputs and build metadata; do not promise
  bit-for-bit identical signed/notarized artifacts without proving it.
- Dependency maintenance, vulnerability triage, supported-version windows,
  deprecation, maintainer handover, and end-of-maintenance policy.
- Optional funding without support/delivery guarantees; no CLA for current docs.

### Acceptance criteria

A fresh user can verify/install without bypassing macOS security controls.
Artifacts correspond to the recorded source/checksums, notices and required source
are available, and every compatibility claim has physical-device evidence.
Recovery instructions and private security reporting work.

## M8 — Expand validated coverage

**Dependencies:** a qualified initial release. **Status:** not started.

- Qualify each additional module/expansion board with the same evidence process.
- Qualify Windows/Linux separately: drivers, serial permissions, packaged native
  dependencies, host security behavior, and physical devices.
- Consider catalogs only after endpoint ownership, HTTPS verification, publisher
  authenticity, firmware rights, cache behavior, and service loss are resolved.
- Require separate proposals for modem, expansion firmware, OTA, and manufacturing.

**Acceptance criterion:** every newly advertised combination has a reviewed
validation record and support-matrix update.

## Verification strategy

| Layer | Evidence | Does not prove |
| --- | --- | --- |
| Repository checks | Links, style, files, workflow hygiene | Runtime correctness |
| Pure core tests | Parser, plans, bounds, preservation | USB/hardware behavior |
| Simulated transport | Timeouts, retries, disconnects, journals | Physical reset timing |
| Native host CI | Architecture, packaging, imports, startup | A physical module update |
| Physical qualification | Backup/update/readback/boot/preservation | Other revisions or drivers |
| Distribution checks | Signing, notarization, clean installation | Firmware authenticity |

Record tool commit/artifact hash, package origin/hash, host OS/architecture,
drivers/bridge, module/expansion revisions, flash/layout, operation intent,
backup verification, readback, boot/preservation/recovery results, tester/date,
limitations, and independent review. Public reports go in `docs/validation/` once
results exist; raw backups and secret-bearing logs stay private and local.

## Initial implementation backlog

This is a proposed backlog; issues and additional owners are not yet assigned.

| ID | Priority | Deliverable | Depends on |
| --- | --- | --- | --- |
| P01 | Blocker | Per-file source/license decision | None |
| P02 | Blocker | Authorized fixture inventory | P01 |
| P03 | High | Python package and runtime CI | P01 |
| P04 | High | Pycom transport adapter comparison | P03 |
| P05 | High | Validated parser and operation planner | P02–P03 |
| P06 | High | Discovery and explicit probing | P04 |
| P07 | High | Verified backup/preservation | P05–P06 |
| P08 | High | Flash executor and failure recovery | P07 |
| P09 | High | First ARM physical qualification | P08 |
| P10 | High | Native packaging and universal audit | P03, P09 for release |
| P11 | Medium | GUI ADR and accessible frontend | P06–P08 |
| P12 | High | Signing, notarization, SBOM, release CI | P01, P09–P10; P11 for GUI |
| P13 | High | Clean-host Intel/ARM qualification | P10–P12 |
| P14 | Medium | Further modules and Windows/Linux | P13 |

## Risks, decisions, and definition of done

| Risk/decision | Response | Gate |
| --- | --- | --- |
| Unresolved additional license terms | Exclude material; obtain permission or choose another implementation | M0 |
| GUI source unavailable | New frontend over a qualified core | M6 |
| Thin native dependencies | Rebuild verified libraries, change toolkit, or separate native builds | M5 |
| Device-specific data damage | Preservation plan, verified backup, protected ranges, recovery tests | M3–M4 |
| Malformed/wrong-target package | Fail closed before I/O | M2 |
| Vendor endpoints unavailable | Local packages remain the first release path | M2, M7 |
| Local firmware unobtainable | Metadata/hash registry, authorized sources, documented source-build limits | M0, M2 |
| Encrypted/protected device | Reject unsupported operations without eFuse changes | M3–M4 |
| Hardware/Intel host unavailable | Narrow scope and mark combination untested | M4–M5 |
| Developer ID unavailable | Label test artifacts; do not claim notarized public distribution | M7 |
| Maintainer capacity changes | Publish support boundaries and handover/deprecation guidance | M7–M8 |

ADRs must settle Python versions, minimum macOS, GUI toolkit, dependency reuse,
package trust, firmware redistribution rights, descriptive application branding,
and support window. Each records
alternatives, evidence, decision, consequences, and a revisit trigger.

No calendar estimate is defensible before M0 and representative hardware access.
A milestone is done only when artifacts exist, acceptance criteria pass, limitations
are recorded, and a maintainer reviews the evidence. Keep planned, implemented,
host-tested, device-tested, and released states distinct in every public claim.
