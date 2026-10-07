# Source provenance and reuse boundaries

**Investigation date:** 2026-10-06. Recheck mutable services and dependencies before use.

## Repository lineage

This is a GitHub fork of
[`pycom/pycom-firmware-updater`](https://github.com/pycom/pycom-firmware-updater).
The baseline is commit
[`7601e335636c487e512cf8b781b2fd3f822f7e18`](https://github.com/pycom/pycom-firmware-updater/commit/7601e335636c487e512cf8b781b2fd3f822f7e18).

At that baseline the complete tree contains only `README.md` and `CHANGELOG.md`.
The six published commits and both public branches contain no desktop application
source or build recipe. Upstream is archived. Its downloadable installers are
historical binaries, not a source distribution for rebuilding the GUI.

The original README is preserved verbatim as [UPSTREAM_README.md](UPSTREAM_README.md).
The root [CHANGELOG.md](../CHANGELOG.md) remains unchanged. This fork's `main`
descends from the original `master`; the fork's default branch was renamed to
`main` on GitHub for community collaboration. Upstream branches/tags are not altered.

## Organization search scope

The investigation inspected default-branch trees in 42 public Pycom repositories
and 58 alternate branches across the relevant firmware/Pymakr repositories.
The findings included the CLI engine below, Pymakr IDE/extension source, documentation,
screenshots, and installer recipes for Pymakr. No source for the independent desktop
Firmware Updater was found in that inspected material. This does not establish
that no unpublished, private, deleted, or differently hosted source exists.

Method: list repositories with `gh api 'orgs/pycom/repos?per_page=100'` (all 42 fit
in one page at the investigation date), including archived repositories and public
forks. Inspect each nonempty default branch through the recursive Git trees API.
Inspect alternate branches in the updater, firmware, Pymakr IDE/kitchen/extensions,
LoPy, WiPy, and libraries repositories. Search paths for updater/firmware/PIC names,
then read relevant files and the updater repository's six commit trees. Recursive
tree responses were not truncated. Indexed code search is supplementary because
it may omit archived material; absence from its results is not decisive.

## Candidate engine (not imported)

Repository: [`pycom/pycom-micropython-sigfox`](https://github.com/pycom/pycom-micropython-sigfox).
Branch inspected: `Dev`. Pinned revision:
`a37510c092bcec00671c924accb97dcdfa2f4b5d`.

| File | Observed role | Header/license declaration |
| --- | --- | --- |
| [updater.py](https://github.com/pycom/pycom-micropython-sigfox/blob/a37510c092bcec00671c924accb97dcdfa2f4b5d/esp32/tools/fw_updater/updater.py) | Package scripts, partitions, configuration, CLI | GPLv3 or later with Pycom additional terms |
| [esptool.py](https://github.com/pycom/pycom-micropython-sigfox/blob/a37510c092bcec00671c924accb97dcdfa2f4b5d/esp32/tools/fw_updater/esptool.py) | ESP32 serial bootloader implementation | GPLv2 or later |
| [pypic.py](https://github.com/pycom/pycom-micropython-sigfox/blob/a37510c092bcec00671c924accb97dcdfa2f4b5d/esp32/tools/fw_updater/pypic.py) | PIC/expansion-board communication | GPLv3 or later with Pycom additional terms |
| [`__init__.py`](https://github.com/pycom/pycom-micropython-sigfox/blob/a37510c092bcec00671c924accb97dcdfa2f4b5d/esp32/tools/fw_updater/__init__.py) | Package initializer | Include in per-file import review |

The updater imports pyserial, its accompanying esptool/PIC modules, and optionally
humanfriendly. It includes Python 2/3 branches; current Python compatibility has
not been tested. It accepts legacy and flash-size-specific package scripts and
exposes backup/configuration operations. Those features need qualification.

Review [Pycom Licences v2.2.pdf](https://github.com/pycom/pycom-micropython-sigfox/blob/a37510c092bcec00671c924accb97dcdfa2f4b5d/Pycom%20Licences%20v2.2.pdf)
and the additional terms referenced by the file headers. A file-level declaration,
the referenced license version, and a repository-level license may differ; resolve
that before import. This inventory records declarations, not a completed legal clearance.

The license review should classify the referenced additional terms and their
effect on the intended reuse/distribution, including applicable GPLv3 Section 7
questions. Record the exact text/version, copyright holder, reviewer, and decision.
Do not infer a right to remove terms or a combined-work license from this plan.

## Import and redistribution checklist

1. Record immutable source revision, per-file hashes, copyright, and exact terms.
2. Resolve Pycom-specific additional terms and required corresponding-source notices.
3. Document local modifications and preserve required attribution.
4. Establish firmware and fixture redistribution rights independently of tool rights.
5. Select compatible runtime/application licensing and bundle required texts.
6. Exclude unresolved source/binaries from imports and release artifacts.

Do not treat extracting an installed application as permission to relicense or
redistribute it. No Pycom executable, firmware, or engine code is included in this
documentation-only community change.

## Primary implementation references

- [PyInstaller macOS multi-architecture support](https://pyinstaller.org/en/stable/feature-notes.html#macos-multi-arch-support): universal2 inputs and architecture validation; finished onefile executables cannot be combined with `lipo`.
- [Apple notarization documentation](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution): distribution signing/notarization process.
- [GitHub-hosted runner reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners): ARM and Intel labels must be checked when CI is implemented.
- [pyserial port-opening behavior](https://pyserial.readthedocs.io/en/latest/pyserial_api.html#serial.Serial.open): DTR/RTS configuration and OS/driver glitch limitations.
- [Pycom CLI documentation](https://github.com/pycom/pycom-documentation/blob/publish/content/advance/cli.md): historical command behavior, not present-day host qualification.

Online references are mutable. Release manifests must pin the versions actually
used rather than relying on the current contents of these documentation pages.
