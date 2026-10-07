# Historical installer recovery

**Status:** static research and partial decompilation, not a runnable updater.
**Observed:** 2026-10-06. **Upstream asset:** `FwUpdater-mac.pkg`, release `v1.0.3`.

This directory records what was recovered from the public historical macOS
installer at the maintainer's request. It helps reconstruct a maintained **GUI
application for Apple Silicon**, preserving existing Pycom modules as Intel-only
applications lose their Rosetta compatibility path.

The separate [classic desktop wizard](../classic-gui-1.16.6/README.md) was also
recovered. This directory concerns the Pybytes service only, not that GUI artifact.

## Evidence and contents

| Item | Result |
| --- | --- |
| Installer | 39,005,017 bytes; SHA-256 `0dbdb6f3fce501627303f117d1b1cbefcddbcc4261305811faaa80b93a41bf3e` |
| Executable | `pycom-fwtool-svc`; 39,249,264 bytes; Mach-O x86_64 |
| Executable SHA-256 | `19f81764a45ee8781362ef5afc2b3f47d0b25997938ff828979ac8a9741a9db6` |
| Packaging/runtime | PyInstaller archive; Python 3.9; PySide2/Qt libraries |
| Outer archive | 155 entries, inventoried with extracted-content hashes |
| Embedded PYZ | 513 modules, inventoried with marshalled-content hashes |
| Selected application candidates | 24 modules; 215 code-object records |
| Recovered references | 24 disassemblies, 23 automatic Python previews, 10 diagnostic files |
| Credential handling | Two embedded credential literals redacted before producing public text |
| Execution/hardware | Installer, application, and recovered code never executed; no device accessed |

The [manifest](manifest.json) records the release/asset IDs, immutable tag commit,
download URL, input hashes, tool revision, normalizations, module symbols, individual
decompiler results, and public-artifact hashes. The release tag is `v1.0.3`, but
the installer and several application constants say `1.0.0`; these are distinct
observed version fields, not a corrected or inferred version.

## Reading the recovered files

All recovered text is in [recovered/](recovered/). Files ending in:

- `.dis.txt` contain CPython 3.9 disassembly of the decoded code objects.
- `.py.txt` contain automatic decompiler output, kept as text to avoid accidental imports.
- `.diagnostics.txt` contain warnings/errors emitted by the decompiler.

Start with [the entry point](recovered/start.dis.txt),
[server](recovered/server.dis.txt), [actions](recovered/utils.actions.dis.txt),
[results](recovered/classes.result.dis.txt), and [tray](recovered/tray.dis.txt).
See [findings and GUI reconstruction](../../docs/RECOVERY_FINDINGS.md).

The selection includes the entry script and candidate application roots `classes`,
`errors_lib`, `npy_programmer`, `programmer`, `pypic`, `server`, `settings`, `tray`,
`updater`, and `utils`. This classification does not establish their authorship or
license. Third-party Python/native libraries and `esptool_lib` are inventoried,
but their source/binaries are not copied into this directory.

## Completeness and limitations

Of 24 candidates, 20 automatic outputs parse syntactically. That does **not** mean
20 faithfully recovered modules: several omit exception handlers or whole function
bodies. `server`, `utils.esp_utils`, and `utils.utils` produce invalid Python;
`utils.hosts` crashes the decompiler and produces no preview. All 24 have disassembly.

Even the warning-free `start` preview mistranslates a keyword call into an invalid
argument expansion. Use its disassembly to see `Thread(target=...)`. Do not run
any preview or treat exit code zero, valid syntax, or silence as proof of equivalence.

Disassembly preserves instructions and symbols more directly, but credentials,
source build paths, and memory addresses were intentionally normalized. Comments,
the original build project, and a complete browser GUI are not recovered. No
execution, protocol interoperability, library modernization, host compatibility,
signing, or hardware behavior has been validated.

## Rights and reuse boundary

These Pycom-derived reference texts are **not covered by this fork's MIT grant**.
They use `LicenseRef-Pycom-Unresolved` to make unresolved licensing explicit; this is not a license
or a permission to reuse them. Original rights remain with their respective holders.

Publication is a recorded, maintainer-requested research exception, not completion
of the M0 runtime reuse/redistribution gate. No maintained application imports these
files. The installer references `LICENSE.txt`, but that file was not present in the
expanded package. Its conclusion contains Pybytes service terms; no open-source
redistribution grant for the local application was identified in the inspected text.

Before moving any recovered material into runtime code or releasing a derivative
application, resolve the applicable terms, attribution, and source obligations.
See [the decision record](../../docs/decisions/0001-installer-reference-recovery.md)
and [licensing scope](../../LICENSE.md). A separately reviewed, originally written
GUI remains an available route; exposure to recovered code is not a clean-room claim.

## Reproduction

Use a local directory outside your checkout. Download only the historical public
asset, verify its SHA-256, and expand it with `pkgutil --expand-full`; this does not
install it or run its post-install script. Do not use `installer`, `open`,
`launchctl`, or the extracted application for this research.

```sh
mkdir -p /tmp/pycom-recovery
curl --fail --location \
  https://github.com/pycom/pycom-firmware-updater/releases/download/v1.0.3/FwUpdater-mac.pkg \
  --output /tmp/pycom-recovery/FwUpdater-mac.pkg
shasum -a 256 /tmp/pycom-recovery/FwUpdater-mac.pkg
pkgutil --expand-full /tmp/pycom-recovery/FwUpdater-mac.pkg /tmp/pycom-recovery/expanded
```

The expected package hash appears above. Stop on mismatch: release assets can be
replaced independently of Git history. Keep inputs and raw intermediates private.

The inspection tool needs Python **3.9** to decode this archive's code objects.
Python 3.9 is used only as an isolated research decoder, not a proposed production
runtime. Optional decompilation uses [zrax/pycdc](https://github.com/zrax/pycdc/tree/b4289760970dbc399684f1e155ec6d1ea1cc787e),
built locally at commit `b4289760970dbc399684f1e155ec6d1ea1cc787e` with CMake.
That third-party tool retains its GPLv3 license and is not vendored here.

From the repository root, with that Python available as `python3.9`:

```sh
python3.9 tools/analyze_installer.py \
  /tmp/pycom-recovery/expanded/FwUpdater-mac.pkg/Payload/Library/FwUpdater-mac/1.0.0/pycom-fwtool-svc \
  --output /tmp/pycom-recovery/analysis
```

Add `--decompiler /absolute/path/to/pycdc` for optional previews. The tool invokes
only the explicitly supplied decompiler, never the analyzed application. It loads
marshalled objects as data and disassembles them; it does not execute/import them.
Use a resource-limited research environment for other inputs. Automatic redaction
is a starting point, not a general secret detector; review output before publication.

The committed snapshot adds reference notices and provenance metadata, omits empty
outputs, and records file hashes. No `.pkg`, executable, `.pyc`, marshalled code,
firmware image, icon, certificate, private key, or original credential is committed.

The publication transform is scripted, with a separate schema version:

```sh
python3 tools/publish_reference.py /tmp/pycom-recovery/analysis \
  --provenance research/installer-v1.0.3/provenance.json \
  --output /tmp/pycom-recovery/reference
```

The two literal credential fallbacks in `settings` were checked against the decoded
instructions and replaced on exact constant matches. Credential-related settings,
server, host helpers, and PEM/userinfo contexts were reviewed by the coding assistant
on 2026-10-06 before publication. This is a scoped static review, not a general
secret detector or independent human/security approval. A CI PEM scan and output
hash checks supplement it; they do not certify arbitrary inputs as secret-free.
