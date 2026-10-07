# Classic desktop GUI recovery

**Status:** static recovery of the historical graphical updater; not a working port.
**Observed:** 2026-10-06. **Download filename version:** `1.16.6`.

This is the separate **Pycom Firmware Update.app** desktop wizard. It is different
from the Pybytes service in the GitHub `v1.0.3` installer. Its code is a much closer
reference for the GUI this project aims to keep available natively on Apple Silicon
as macOS ends general Rosetta support.

## Artifact provenance

The macOS link in [Pycom's device update documentation](https://docs.pycom.io/updatefirmware/device/)
redirected to
[pycom_firmware_updater_1.16.6.dmg](https://software.pycom.io/downloads/pycom_firmware_updater_1.16.6.dmg).
The image was downloaded, checksummed, and mounted read-only without opening or
installing its application. Its main executable matched the SHA-256 of the installed
copy inspected locally; all published recovery here uses the **public download**.
No local user configuration, logs, backups, or device state were read or committed.

| Field | Observation |
| --- | --- |
| DMG size | 36,607,185 bytes |
| DMG SHA-256 | `af75690904870ffd3a4a76348712a374bc4a3eb063d0be111e029ad4e100b473` |
| Main executable size | 30,307,488 bytes |
| Main executable SHA-256 | `7310b09a852785f26e3b5e41eb5d86a1cd9b8f1fb3363455ca5e27bc831b7a0f` |
| Bundle identifier | `com.pycom.fwtool` |
| Info.plist short version | `0.0.0`; distinct from the download's `1.16.6` filename |
| Native architecture | Mach-O x86_64 |
| Frameworks/runtime | Python 2.7, PyQt4, Qt4 |
| Outer archive / embedded modules | 137 entries / 619 PYZ modules |
| Selected GUI/core candidates | 11 modules, 275 code-object records |
| Recovery outputs | 11 Python previews and 11 cross-version disassemblies |

See the [manifest](manifest.json) and [provenance input](provenance.json) for hashes,
tool versions, symbol inventories, and exact input identity. Download URLs are
mutable; verify hashes before comparing or reproducing this snapshot.

## What was recovered

| Candidate module | Role observed in decoded code |
| --- | --- |
| [pycom_fwtool](recovered/pycom_fwtool.py.txt) | `CustomWizard`/`CustomWizardPage`, GUI pages, callbacks, selections, validation, progress, and result handling |
| [DeviceInfoQuery](recovered/DeviceInfoQuery.py.txt) | Device metadata/configuration query worker |
| [DeviceUpgrade](recovered/DeviceUpgrade.py.txt) | Upgrade execution worker and progress/result callbacks |
| [FetchFiles](recovered/FetchFiles.py.txt) | Firmware/metadata fetching and local file loading |
| [RunInWorker](recovered/RunInWorker.py.txt) | Qt worker abstraction |
| [LoadingSpin](recovered/LoadingSpin.py.txt) | Qt loading indicator |
| [env_settings](recovered/env_settings.py.txt) | Application paths and argument container |
| [pyconf](recovered/pyconf.py.txt) | Local JSON settings handling |
| [misc](recovered/misc.py.txt) | Utility and diagnostic functions |
| [updater](recovered/updater.py.txt) | CLI/package/flash/configuration logic bundled with the GUI |
| [pypic](recovered/pypic.py.txt) | Expansion-board PIC communication |

The wizard contains welcome, device type, LoRa/Sigfox region, setup instructions,
license, communication, board information, Pybytes registration, advanced settings,
local-file/download, upgrading, and result pages. Local firmware selection already
exists in the recovered historical UI. Its existence is not a current compatibility
or preservation guarantee.

All 11 were processed without a raised decompiler error by `uncompyle6 3.9.3` and
their normalized previews passed an offline grammar check using
CPython 3.9.25's permissive Python-2-compatible `lib2to3` parser. This verifies
grammar only, not compilation with a Python 2 interpreter. Bytecode/control-flow
equivalence, live GUI startup, endpoint behavior, and hardware operations remain
unverified. An initial `pycdc` attempt failed partway through the wizard; it is not
the source of this committed GUI preview.

The selected source previews retain Python 2/PyQt4 semantics. No port to Python 3,
Qt6, ARM, universal2, or a signed/notarized application is claimed. The decoder's
module-level bare `return` statements were removed as an explicit normalization;
they cannot appear in a Python source module. See the disassembly before interpreting
any recovered expression as faithful behavior.

## Privacy and rights

The PYZ archive uses historical PyInstaller AES-CFB8 packaging. Its embedded key
module was decoded **as data** to unpack modules; it was not imported/executed,
and the key/module/raw bytecode are not exported. No vendor credentials were used.
The narrow credential-assignment heuristic matched zero literals in these selected
GUI candidates; this is not a general guarantee that arbitrary artifacts are safe.
The configuration module and credential/token/PEM contexts were separately reviewed
as static code. Public recovery includes no user configuration or original PEM block.

Recovered text and derived symbol inventories have unresolved original rights,
identified with `LicenseRef-Pycom-Unresolved`. This is a notice, not a license grant.
They are excluded from MIT and are not admitted as runtime source. Public download,
research recovery, and the maintainer's request do not establish reuse permission.
See [LICENSE.md](../../LICENSE.md) and [ADR 0001](../../docs/decisions/0001-installer-reference-recovery.md).
No icons, binaries, native dependencies, firmware, or archive key are committed.

## Reproduction

Download the linked DMG to a private research directory, verify the hash above,
and mount it read-only with browsing/auto-opening disabled. Inspect only its files.
On macOS, the commands used were:

```sh
curl --fail --location \
  https://software.pycom.io/downloads/pycom_firmware_updater_1.16.6.dmg \
  --output /tmp/pycom-classic.dmg
shasum -a 256 /tmp/pycom-classic.dmg
hdiutil attach -readonly -nobrowse -mountpoint /tmp/pycom-classic /tmp/pycom-classic.dmg
```

Create an isolated research environment with Python 3.13 and the pinned
[research requirements](../../tools/legacy-research-requirements.txt). These are
decoder dependencies, not application/runtime requirements. From the repository root:

```sh
python3.13 -m venv /tmp/pycom-research-env
/tmp/pycom-research-env/bin/pip install -r tools/legacy-research-requirements.txt
/tmp/pycom-research-env/bin/python tools/analyze_classic_gui.py \
  '/tmp/pycom-classic/Pycom Firmware Update.app/Contents/MacOS/Pycom Firmware Update' \
  --output /tmp/pycom-classic-analysis
python3 tools/publish_reference.py /tmp/pycom-classic-analysis \
  --provenance research/classic-gui-1.16.6/provenance.json \
  --output /tmp/pycom-classic-reference
hdiutil detach /tmp/pycom-classic
```

Detach the read-only image after inspection. Do not execute the application,
`pycom-fwtool-cli`, or any recovered module. Review any new output before publication.
The publication transform prepends rights notices, omits empty text, and hashes the
final bytes; the metadata input records the separate provenance/validation findings.
Library/runtime updates may change generated text without changing the original input.

Reproduce the grammar-only check with isolated CPython 3.9 (the Python 3.13
decoder environment does not contain `lib2to3`):

```sh
python3.9 tools/check_legacy_syntax.py research/classic-gui-1.16.6 \
  --report /tmp/pycom-classic-syntax.json
```

The committed [per-module grammar report](syntax-report.json) records the result
and its scope. Decoder versions are captured from the actual analysis environment
in the manifest. Literal whitespace is preserved; reference Git attributes keep
LF byte identity across platforms while avoiding edits to generated expressions.

The next implementation decisions are in [GUI reconstruction findings](../../docs/RECOVERY_FINDINGS.md)
and the [maintenance plan](../../docs/MAINTENANCE_PLAN.md). Recovery supplies reference
behavior; qualification and a maintained GUI still require implementation work.
