# ADR 0001: Keep installer recovery as reference research

**Date:** 2026-10-06. **Status:** adopted for research scope; runtime licensing open.

## Context and authorization

The maintainer explicitly requested decompilation of the historical macOS
application and addition of recovered results to this personal fork. The intended
product remains a GUI, with native Apple Silicon support as macOS ends general
Rosetta support. Public Git history does not provide the desktop/service source.

The GitHub installer contains a Python service/tray application, not a recovered
complete graphical frontend. A separate public `1.16.6` DMG contains the classic
Python 2.7/PyQt4 desktop wizard; its eleven GUI/core modules were also recovered.
Automatic decompilation is partial or unqualified and can silently
mistranslate keyword calls. Embedded credential fallbacks were also discovered.

## Decision

Publish the original inspection tool, synthetic tests, an input/output hash
manifest, research findings, and **redacted text reference snapshots**. This is a
specific maintainer-requested exception to the repository's initial no-import
research boundary. No exception is made for importing an engine into runtime code
or releasing a rebuilt application. M0 reuse/redistribution clearance remains open.

Keep reference outputs under `research/installer-v1.0.3/` and
`research/classic-gui-1.16.6/`, with `.py.txt` and
`.dis.txt` extensions, original provenance, and `LicenseRef-Pycom-Unresolved` notices. The MIT grant
applies to original community tooling/docs, not Pycom-derived text. Do not assert
that the request, the asset's public availability, or decompilation grants rights
over the original code. Treat rights-holder/license resolution as a distinct task.

Do not commit raw binaries, marshalled bytecode, dependency libraries, icons,
certificates, private keys, or original credential literals. Do not install or run
the original service, use its credentials, alter hosts files, or connect hardware.

## Alternatives

- Only record metadata: smaller rights surface but omits the requested recovery
  evidence and limits reproducibility of GUI/core research.
- Import previews as an engine: rejected because of unresolved rights, incomplete
  functions, and unvalidated hardware behavior.
- Repack the old service for ARM: does not recover a full GUI and retains obsolete
  dependencies/service coupling; it cannot satisfy the desktop acceptance target.
- Treat the classic wizard as a finished port: rejected because its Python 2/Qt4
  runtime, component terms, preserved behavior, and native packaging need qualification.

## Consequences and revisit trigger

The repository contains derived reference material with unresolved terms. It is
not a license-cleared source release of the historical application. Contributors
must not move references into runtime code or label them MIT/GPL by assumption.
This is also not a clean-room reimplementation process.

Revisit when exact applicable terms or rights-holder permission are established,
when a complete public GUI/source project is located, or when independent decoder
and fixture evidence can qualify a specific reconstructed component. Record any
runtime import separately, including its redistribution basis, notices, changes,
and validation. Review/remove affected references if their rights status requires it.
