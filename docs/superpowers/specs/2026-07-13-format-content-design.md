# format-content Skill Design

## Goal

Create a standalone, installable Agent Skill named `format-content` that converts Markdown into WeChat Official Account HTML using only the red-and-white theme extracted from `isjiamu/gzh-design-skill`.

## Scope

The Skill accepts Markdown text or a readable `.md` file. It does not accept Word, PDF, legacy `.doc`, or unstructured plain text. It does not offer theme selection or theme generation.

The red-and-white theme behavior remains aligned with the upstream Skill: article structure parsing, article-type recipes, section numbering, highlighted keywords, table of contents, quotations, code, images and GIFs, lists, tables, Chinese punctuation normalization, and a single author/CTA footer.

## Architecture

- The repository root owns public documentation, licensing, tests, and development records.
- `format-content/SKILL.md` owns the fixed-theme workflow, input contract, failure paths, output contract, and verification loop.
- `format-content/references/theme-red-white.md` remains the authoritative red-and-white component library.
- `format-content/references/common-components.md` supplies code, media, and small-label components shared by the upstream design.
- `format-content/scripts/component_lint.py` checks component-library source HTML.
- `format-content/scripts/validate_gzh_html.py` checks the generated clean HTML fragment.
- `format-content/scripts/wrap_preview.py` and `format-content/assets/preview-template.html` create the browser preview with a rich-text copy button.

The Skill is runtime-neutral. Its instructions must not depend on Codex-, Claude Code-, or Cursor-specific tool names. Optional Codex UI metadata may exist under `agents/` without changing the portable workflow.

## Outputs

For an input named `article.md`, successful execution produces exactly these two deliverables in the user's working directory:

1. `article_排版_红白色系(red-white).html`: a clean `<section>…</section>` body fragment with no document wrapper.
2. `article_排版_红白色系(red-white)_预览.html`: a complete browser page that renders the same body and provides a “复制到公众号” button.

The preview copies rendered rich text to the clipboard. The Skill does not call WeChat APIs and does not automatically publish or create a draft.

## Verification

Completion requires:

- Skill structure validation succeeds.
- All bundled Python files compile.
- Component lint reports zero errors.
- A fresh Agent run formats a representative Markdown fixture and emits both named HTML files.
- The clean body passes `validate_gzh_html.py` with zero errors and zero warnings.
- The preview embeds the clean body unchanged inside the copy target.
- A clean installation from the public GitHub URL succeeds in isolated Agent homes.

## Distribution and License

The installable Skill is the nested directory `format-content/` inside the public repository `BruceL017/format-content`. The repository root MUST NOT contain `SKILL.md`: `npx skills` 1.5.16 special-cases a root Skill and copies only `SKILL.md`, dropping bundled references, scripts, and assets. With the nested directory, the installer copies the complete Skill while the installation command remains the repository URL used by the upstream project.

This project is a modified extraction of `isjiamu/gzh-design-skill`. It retains AGPL-3.0 licensing, upstream copyright notices, attribution, and a notice describing the reduced fixed-theme scope. License and notice files remain at the repository root and are also bundled in the installed Skill directory.

## Non-goals

- Supporting any theme other than red-and-white.
- Deterministically compiling Markdown without an Agent.
- Writing or rewriting the article's substantive content.
- Converting Word, PDF, or plain text into Markdown.
- Publishing to WeChat through an API.
- Extending upstream behavior beyond what the fixed red-and-white path needs.
