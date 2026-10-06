# Folder README Template

## Instructions for the AI

Inspect the folder's immediate files, source contents, and subfolder README documents before writing. Use the structure below, starting with `# Directory Summary` and keeping all five sections in order. Replace placeholders and example rows with verified information; do not include these instructions in the generated README.

Before creating the inventory, exclude files matching any of these patterns:

```text
*.aux
*.log
*.synctex.gz
*.toc
*.out
*.lof
*.lot
*.synctex
*.fls
*.fdb_latexmk
*.pdf
*.gz
```

Treat all matching files, and any similar generated LaTeX compilation artifacts, as build/output files rather than source files. Ignore them throughout the README: do not list, describe, link to, or summarize them in any section, including the directory tree and public-command inventory. Base folder summaries on the remaining source files and maintained assets. Apply this rule even when generated files are tracked in version control or mentioned in an existing README.

- **Purpose:** Write one short sentence explaining the folder's role, its main contents, and their intended use in the project.
- **Files:** Include every immediate file remaining after the artifact exclusions, including the actual README filename. Identify its format (for example, LaTeX, Markdown, Python, or PNG). Describe its concrete function or contents in one concise sentence, using verbs such as “Defines,” “Draws,” “Computes,” or “Summarizes.” Name the relevant subjects, outputs, or distinguishing variants; avoid vague descriptions such as “Contains code.” Read contents rather than inferring purpose from filenames alone.
- **Folders:** Include every immediate subfolder in a table. Summarize its role or contents in one concise sentence and link to its README when one exists. Use `None.` when there are no subfolders.
- **Directory Structure:** Show the folder's actual name, all non-excluded immediate files, and immediate subfolders in a `text` tree, matching the tables. Mark subfolders with a trailing `/`; do not expand their contents.
- **Public Commands:** Include one row per file in the Files table. List all public commands defined by that file, such as reusable LaTeX macros or callable entry points, using their exact names in backticks, separated by commas. Include public aliases and variants; omit internal helpers, imported commands, and usage examples. Use `None.` for files that define no public commands.

Use concise English and consistent domain terminology. Keep the README descriptive; add no extra sections, tutorials, or unsupported claims. Use actual filenames throughout, even when they differ from `README.md`.

Order files first by type (alphabetically by the type labels used in the Files table), then alphabetically by filename within each type, ignoring case. Use this same file order in the Files table, Directory Structure tree, and Public Commands table. Sort subfolders alphabetically by name in the Folders table and place them before the grouped files in the tree.

Write links relative to the generated README's folder using forward slashes: [`example.tex`](example.tex), [`module/`](module/), [`README-module.md`](module/README-module.md), or [`README-parent.md`](../README-parent.md). Use linked filenames in tables and link relevant related documents within descriptions when helpful. Only link to existing targets, apart from the README being generated; never use absolute paths. If a subfolder has no README, link to the folder itself and write `None.` in its README column.

## Output Template

# Directory Summary

## Purpose

[One-sentence description of this folder's role and intended use.]

## Files

| File | Type | Purpose |
|---|---|---|
| [`example.tex`](example.tex) | LaTeX | Defines reusable commands for [specific task or output]. |
| [`README-folder.md`](README-folder.md) | Markdown | Summarizes this directory. |

## Folders

| Folder | Purpose | README |
|---|---|---|
| [`module/`](module/) | Provides [specific functionality or materials]. | [`README-module.md`](module/README-module.md) |

## Directory Structure

```text
folder_name/
├── module/
├── example.tex
└── README-folder.md
```

## Public Commands

| File | Commands |
|---|---|
| [`example.tex`](example.tex) | `\ExampleCommand`, `\ExampleVariant` |
| [`README-folder.md`](README-folder.md) | None. |
