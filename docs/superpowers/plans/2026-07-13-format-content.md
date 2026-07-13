# format-content Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, verify, and publicly release a standalone `format-content` Skill that formats Markdown with the upstream red-and-white WeChat theme and emits the original two HTML deliverables.

**Architecture:** Keep the Agent-driven upstream rendering model, but hard-wire the only theme to `theme-red-white.md`. Bundle the upstream common components, source and output validators, and preview wrapper so the Skill has no runtime dependency on the upstream repository.

**Tech Stack:** Markdown Skill instructions, Python 3 standard library, inline HTML/CSS, Git, GitHub CLI, `npx skills` installer.

## Global Constraints

- Create and modify files only under `/Users/hkd-xiaobei/Documents/context-skills/format-content`.
- Accept only Markdown text or readable `.md` files.
- Use only the red-and-white theme; do not offer theme selection or generation.
- Preserve the upstream clean-body and copy-preview output behavior.
- Do not call a WeChat publishing API.
- Retain upstream AGPL-3.0 licensing, copyright, attribution, and modification notice.
- Use `253661133+BruceL017@users.noreply.github.com` for every commit author and committer email.
- Publish the final repository publicly as `BruceL017/format-content`.

## Installer Compatibility Amendment

`npx skills` 1.5.16 installs only `SKILL.md` when a cloned repository itself is detected as the Skill root. A controlled `/tmp` experiment proved that a nested `format-content/SKILL.md` causes the installer to copy the complete Skill directory. Final layout therefore MUST keep public repository files at the root and the installable Skill under `format-content/`; all earlier Skill-file paths become `format-content/<path>` after the migration. The repository URL and installed Skill name remain unchanged.

---

### Task 1: Scaffold the portable Skill and import upstream assets

**Files:**
- Create: `SKILL.md`
- Create: `agents/openai.yaml`
- Create: `references/theme-red-white.md`
- Create: `references/common-components.md`
- Create: `scripts/component_lint.py`
- Create: `scripts/validate_gzh_html.py`
- Create: `scripts/wrap_preview.py`
- Create: `assets/preview-template.html`
- Create: `LICENSE`

**Interfaces:**
- Consumes: upstream commit `ba1f417` files from `isjiamu/gzh-design-skill`.
- Produces: a valid Skill skeleton with verbatim reusable theme, component, script, template, and license assets.

- [ ] **Step 1: Initialize the Skill skeleton**

Run the installed `skill-creator` initializer with `format-content` as the exact name and `scripts,references,assets` as resources. Generate only the portable metadata required by the initializer.

- [ ] **Step 2: Add the upstream assets**

Use `apply_patch` to add the exact contents of these upstream files:

```text
references/theme-red-white.md
references/common-components.md
scripts/component_lint.py
scripts/validate_gzh_html.py
scripts/wrap_preview.py
assets/preview-template.html
LICENSE
```

- [ ] **Step 3: Verify asset fidelity**

Run SHA-256 comparisons against the upstream checkout. Expected: every imported reusable asset has an identical hash before any narrowly required standalone-path edit.

- [ ] **Step 4: Commit the imported assets**

Verify `git config user.email`, stage only Task 1 files, commit with `feat: import red-white formatting assets`, then verify `git log -1 --format='%ae'` equals the required noreply address.

---

### Task 2: Author the fixed-theme workflow and public installation surface

**Files:**
- Modify: `SKILL.md`
- Modify: `agents/openai.yaml`
- Create: `README.md`
- Create: `NOTICE`

**Interfaces:**
- Consumes: the imported theme, components, scripts, and preview template from Task 1.
- Produces: a runtime-neutral Skill contract and human-readable GitHub installation instructions.

- [ ] **Step 1: Write the Skill contract**

Define frontmatter with only `name` and `description`. Define explicit Markdown input validation, fixed red-and-white component loading, structure parsing, recipe selection, HTML assembly, zero-warning validation loop, preview wrapping, exact output names, failure exits, positive example, and labeled bad example.

- [ ] **Step 2: Generate Codex UI metadata**

Generate `agents/openai.yaml` from the final Skill using the bundled `skill-creator` generator. The metadata may improve Codex discovery but must not be referenced by the portable workflow.

- [ ] **Step 3: Document installation and attribution**

Write `README.md` with the GitHub install command, supported inputs, exact outputs, usage example, verification behavior, and upstream attribution. Write `NOTICE` identifying the upstream repository, source commit, retained files, modification date, and reduced scope.

- [ ] **Step 4: Commit the workflow**

Verify the noreply email, stage only Task 2 files, commit with `feat: add standalone red-white formatting workflow`, and verify the commit author email.

---

### Task 3: Add deterministic regression coverage

**Files:**
- Create: `tests/test_scripts.py`
- Create: `tests/fixtures/valid-section.html`
- Create: `tests/fixtures/invalid-section.html`
- Create: `tests/fixtures/article.md`

**Interfaces:**
- Consumes: the three bundled Python scripts and preview template.
- Produces: standard-library tests for validator exit codes, preview embedding, component lint, and the representative Markdown fixture used by the behavior test.

- [ ] **Step 1: Write failing integration tests**

Use `unittest` and subprocess calls to assert:

```text
valid-section.html -> validate_gzh_html.py exits 0 with no WARNING
invalid-section.html -> validate_gzh_html.py exits 1
wrap_preview.py -> preview contains the clean section exactly once inside #gzh-content
component_lint.py . -> exits 0 and reports ERROR×0
```

- [ ] **Step 2: Run tests before fixture completion**

Run `python3 -m unittest discover -s tests -v`. Expected: failure because one or more fixtures or exact assertions are not yet satisfied.

- [ ] **Step 3: Complete the minimal fixtures and test harness**

Use only valid inline styles and `<span leaf="">` text in the clean fixture. Include a forbidden `<div>` in the invalid fixture. Make the Markdown fixture exercise headings, quotation, emphasis, list, code, table, and image syntax.

- [ ] **Step 4: Run deterministic verification**

Run:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/*.py
python3 scripts/component_lint.py .
```

Expected: all tests pass, compilation exits 0, and lint reports `ERROR×0`.

- [ ] **Step 5: Commit regression coverage**

Verify the noreply email, commit Task 3 files with `test: cover formatting validation workflow`, and verify the commit author email.

---

### Task 4: Validate the Skill instructions and forward behavior

**Files:**
- Modify only if review findings require it: `SKILL.md`, `agents/openai.yaml`, `README.md`, `NOTICE`
- Generate outside the repository: `/tmp/format-content-eval/*`

**Interfaces:**
- Consumes: the complete Skill and `tests/fixtures/article.md`.
- Produces: a zero-issue prompt review and two valid forward-test HTML files.

- [ ] **Step 1: Run structural validation**

Run the installed `quick_validate.py` against the Skill root. Expected: successful validation with no frontmatter or naming errors.

- [ ] **Step 2: Run prompt-review A–G**

Review `SKILL.md` and `agents/openai.yaml` against the installed `prompt-review` checklist. Apply every BLOCKER, HIGH, and MEDIUM finding that maps to A–G, then re-run until the review ledger has zero open issues.

- [ ] **Step 3: Forward-test with a fresh Agent**

Give a fresh Agent only the Skill path, the representative Markdown path, and an isolated `/tmp/format-content-eval` working directory. Require ordinary user wording rather than revealing expected HTML internals.

- [ ] **Step 4: Verify generated deliverables**

Assert both exact output filenames exist. Run `validate_gzh_html.py` on the clean file and require zero errors and warnings. Extract the preview copy target and compare it byte-for-byte with the clean body after outer whitespace normalization.

- [ ] **Step 5: Commit review fixes**

If Task 4 changed tracked files, verify the noreply email and commit them with `fix: harden format-content skill instructions`. If it changed no tracked files, record the clean review and do not create an empty commit.

---

### Task 5: Publish and verify clean installation

**Files:**
- Modify only if release verification finds a defect: files owned by prior tasks.

**Interfaces:**
- Consumes: the verified local `main` branch.
- Produces: public repository `https://github.com/BruceL017/format-content` and isolated installation evidence.

- [ ] **Step 1: Run the complete pre-publish gate**

Re-run structural validation, unit tests, Python compilation, component lint, clean-output validation, prompt review, `git status -sb`, and the commit-email audit for every local commit.

- [ ] **Step 1a: Reproduce and guard the installer layout bug**

Add a failing repository-layout test that requires no root `SKILL.md`, requires `format-content/SKILL.md`, and requires the nested references, scripts, assets, metadata, license, and notice. Run it before migration and record the expected failure.

- [ ] **Step 1b: Apply the single layout fix and turn the test green**

Move the installable Skill files under `format-content/`, keep repository documentation/tests/licenses at the root, bundle `LICENSE` and `NOTICE` in the nested Skill, and update repository tests to resolve the nested Skill root. Run the layout test, full unit suite, structural validation, compilation, component lint, and fresh-Agent behavior until all pass.

- [ ] **Step 2: Create and push the public repository**

Create `BruceL017/format-content` as public with `main` as the source branch, add `origin`, and push with tracking. Do not create a pull request because this is a new repository release rather than a change to an existing remote.

- [ ] **Step 3: Verify remote state and installable Skill location**

Use GitHub API/CLI to confirm visibility is `PUBLIC`, the default branch is `main`, the remote head matches local `HEAD`, public `format-content/SKILL.md` is accessible, and repository-root `SKILL.md` is absent or returns HTTP 404.

- [ ] **Step 4: Test isolated installation**

In a temporary `HOME`, install from `https://github.com/BruceL017/format-content` with `npx skills add`. Verify the installer discovers `format-content` and writes a complete Skill containing `SKILL.md`, references, scripts, and assets. Repeat discovery for every Agent target the installer reports as supported.

- [ ] **Step 5: Re-run from the installed copy**

Run structural validation, Python tests or equivalent script checks, component lint, and the representative formatting forward test against the isolated installed copy. Any failure returns to the owning task, followed by a new commit, push, and complete re-verification.

- [ ] **Step 6: Report release evidence**

Report the repository URL, installation command, commit hash, noreply email audit, validation commands, test counts, supported installer targets actually observed, and any runtime not behavior-tested.
