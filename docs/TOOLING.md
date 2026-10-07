# Repository tooling

These tools check documentation, research provenance, and the static inspector.
They neither build an updater nor access connected hardware.

## Checks

`npm ci` installs locked development dependencies. `npm run check` runs:

- Markdown style checks over community-authored documents.
- YAML parsing with duplicate-key rejection and minimal workflow/issue-form checks.
- Relative Markdown file/heading links, required project files, final newlines,
  and trailing whitespace.
- SHA-256 preservation of the two inherited documentation artifacts.
- Full-SHA action pinning and Conventional Commit PR titles when `PR_TITLE` is set.
- Synthetic static-inspection tests for malformed archives, unsafe paths,
  credential redaction, and non-execution of recovered code.
- Hashes and completeness of committed research references against their manifest.

External HTTP links are source references, not checked for availability by offline
CI. Review them when their content is used. The link checker handles this repository's
inline Markdown links; new reference-link syntax or raw HTML requires extending it
or adopting a dedicated checker.

## Dependencies and audit

The project uses the `markdownlint` library directly and Node.js file enumeration
rather than an additional CLI/glob dependency tree. YAML parsing uses `yaml`.
Both direct versions are exact and the npm lockfile is committed.

The `katex` override pins version 0.18.2 for markdownlint's transitive math renderer.
This resolves the reported
[KaTeX trust-bypass advisory](https://github.com/advisories/GHSA-238p-pmpm-9mq7)
without suppressing audit findings. Revisit/remove the override when the upstream
dependency chain includes a fixed version naturally. Check lint behavior when
changing it. The current project documents do not use mathematical expressions.

Run `npm audit` when dependencies change; CI also rejects high/critical audit
findings. Dependabot proposes monthly npm and
GitHub Actions updates. A clean audit is a dated result, not a future security
guarantee. Future runtime dependencies require their own checks and support policy.

Inherited `CHANGELOG.md` and `docs/UPSTREAM_README.md` are excluded from style/link
changes and Git whitespace normalization/checks, and protected by content hashes.
They preserve historical upstream material
whose licensing differs from new community work.

## Static installer research

[tools/analyze_installer.py](../tools/analyze_installer.py) inventories an extracted
PyInstaller executable and disassembles selected application candidates without
importing/executing them. Its decoder must match the archive's Python version;
the historical asset needs isolated Python 3.9. The optional external `pycdc`
produces incomplete previews, not a trusted application source tree.

[Reproduction instructions](../research/installer-v1.0.3/README.md) describe hashes,
tools, normalization, and rights boundaries. The installer/application and original
credentials are never executed or used. Raw research intermediates belong outside
the checkout, not in public commits. Automatic redaction does not replace review.

[Classic GUI research](../research/classic-gui-1.16.6/README.md) uses a separate
cross-version decoder and pinned isolated dependencies. Neither legacy Python 2.7
nor Qt4 is adopted as the future application runtime. The publication transform in
`tools/publish_reference.py` distinguishes raw inspection schema 1 from reference
snapshot schema 2 and computes final text hashes.
