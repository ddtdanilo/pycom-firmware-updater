# Support and qualification matrix

**No module or host is currently supported by a community build from this fork.**
The tables below identify candidates and required evidence, not compatibility guarantees.

## Candidate modules

| Module | Target | Current status | Qualification requirements |
| --- | --- | --- | --- |
| WiPy 2 | Initial candidates | Not implemented or tested | Revision, actual flash size/layout, USB/reset strategy |
| WiPy 3 | Initial candidates | Not implemented or tested | Revision, flash/layout, backup/preservation |
| LoPy | Initial candidates | Not implemented or tested | Revision, radio variant, device configuration |
| LoPy4 | Initial candidates | Not implemented or tested | Revision, flash/layout, radio configuration |
| SiPy | Initial candidates | Not implemented or tested | Revision, protection state, radio credential preservation |
| FiPy | Initial candidates | Not implemented or tested | Revision, flash/layout, configuration; modem excluded |
| GPy | Initial candidates | Not implemented or tested | Revision, flash/layout, configuration; modem excluded |
| WiPy 1 | Deferred/out of initial scope | Not supported | Separate architecture and updater assessment |
| Other ESP32 boards | Out of initial scope | Not supported | Separate device model and explicit approval |

Do not infer flash size or firmware compatibility from a marketing name. Probe and
validate each revision and package against its actual layout.

## Host platforms

| Host/distribution | Priority | Current status | Minimum release evidence |
| --- | --- | --- | --- |
| macOS ARM native GUI | Primary product target | Not built or tested | Complete GUI on a clean host without Rosetta plus physical-device qualification |
| macOS Intel native | Transition support | Not built or tested | Native Intel host plus physical-device qualification |
| macOS universal2 GUI | Transition support | Not built or tested | Full GUI/binary slice audit plus both native host qualifications |
| Linux | Later | Not built or tested | Packaging, permissions, bridge/driver, physical device |
| Windows | Later | Not built or tested | Packaging, driver, host security, physical device |

Minimum OS and Python versions remain design decisions. Documentation CI runs on
Linux; that does not establish Linux updater support.

The [installer recovery](RECOVERY_FINDINGS.md) establishes historical x86_64
packaging, not community Intel compatibility. Native ARM prevents dependence on
the ending Rosetta path. Neither static recovery nor documentation CI qualifies
an updater or GUI on any host.

## Expansion boards and connection strategies

FTDI bridges, PIC-controlled expansion boards, and manual bootloader entry need
separate qualification. Record the expansion-board revision, USB VID/PID, bridge,
driver, cable/power setup, baud rate, and reset sequence for every result.

Host USB drivers and expansion-board firmware are prerequisites to investigate;
this project does not currently install drivers or update expansion-board MCUs.

## Operations

| Operation | Intended scope | Current status |
| --- | --- | --- |
| Port enumeration and identity | Initial CLI | Not implemented |
| Local package inspection and dry run | Initial CLI | Not implemented |
| Backup and preservation | Required before supported destructive operations | Not implemented |
| Package flashing and verification | Qualified module/layout combinations only | Not implemented |
| Restore/recovery | Explicitly qualified, identity-checked flows | Not implemented |
| Secure-boot/encryption provisioning or eFuse changes | Outside ordinary updates | Not supported |
| LTE modem, expansion-board MCU firmware, OTA | Separate future proposals | Not supported |
| Vendor cloud activation/network services | Outside updater maintenance | Not provided |

## How support is earned

Use distinct labels: **planned → implemented → host-tested → device-tested → released**.
Device-tested means a traceable physical result for a specific module/host/connection
combination. Released means that evidence qualifies the actual published artifact.

A qualification record must contain the metadata and results listed in the
[plan's verification strategy](MAINTENANCE_PLAN.md#verification-strategy), including
backup, programmed-range readback, preservation, boot, and recovery results.
Do not publish private backups or secret-bearing logs. Maintain separate records
for destructive reset and data-preserving update.

Qualification is bound to an artifact and test conditions. Changes to transport/reset
code, package planning, the bundled engine, packaging toolchain, or supported OS
boundaries require a targeted reassessment before carrying results into a new release.
A regression can change a combination to **withdrawn**; document impact and recovery
guidance. Do not erase the historical record or leave a known-unsafe combination
advertised as currently supported.
