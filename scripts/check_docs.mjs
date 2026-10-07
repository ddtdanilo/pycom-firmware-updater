// SPDX-License-Identifier: MIT
import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { lint } from 'markdownlint/promise';
import { parseDocument } from 'yaml';

const root = fileURLToPath(new URL('..', import.meta.url));
const ignoredDirectories = new Set(['.git', 'node_modules', '.venv']);
const inherited = new Set(['CHANGELOG.md', 'docs/UPSTREAM_README.md']);
const files = [];

async function walk(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const full = path.join(directory, entry.name);
    if (entry.isDirectory() && !ignoredDirectories.has(entry.name)) await walk(full);
    else if (entry.isFile()) files.push(full);
  }
}

await walk(root);
const config = JSON.parse(await readFile(path.join(root, '.markdownlint.json'), 'utf8'));
const markdown = files.filter(file => file.endsWith('.md') && !inherited.has(path.relative(root, file)));
const results = await lint({ files: markdown, config });
let failed = false;
for (const [file, issues] of Object.entries(results)) {
  for (const issue of issues) {
    console.error(`${path.relative(root, file)}:${issue.lineNumber}: ${issue.ruleNames[0]} ${issue.ruleDescription}${issue.errorDetail ? ` (${issue.errorDetail})` : ''}`);
    failed = true;
  }
}

const yamlFiles = files.filter(file => file.startsWith(path.join(root, '.github') + path.sep) && /\.ya?ml$/.test(file));
for (const file of yamlFiles) {
  const document = parseDocument(await readFile(file, 'utf8'), { uniqueKeys: true });
  if (document.errors.length) {
    for (const error of document.errors) console.error(`${path.relative(root, file)}: ${error.message}`);
    failed = true;
    continue;
  }
  try {
    const data = document.toJS({ maxAliasCount: 10 });
    if (file.includes(`${path.sep}workflows${path.sep}`) && (!data.on || !data.jobs || !data.permissions)) {
      throw new Error('Workflow must specify triggers, jobs, and token permissions');
    }
    if (file.includes(`${path.sep}ISSUE_TEMPLATE${path.sep}`) && path.basename(file) !== 'config.yml') {
      if (!data.name || !data.description || !Array.isArray(data.body)) throw new Error('Issue form is missing required metadata/body');
      const ids = data.body.filter(field => field.id).map(field => field.id);
      if (new Set(ids).size !== ids.length) throw new Error('Issue form IDs must be unique');
    }
  } catch (error) {
    console.error(`${path.relative(root, file)}: ${error.message}`);
    failed = true;
  }
}

if (failed) process.exitCode = 1;
else console.log(`Documentation lint passed: ${markdown.length} Markdown files and ${yamlFiles.length} YAML files.`);
