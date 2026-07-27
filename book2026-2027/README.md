# 2026–2027 LaTeX Collection

## Status and contents

**Lifecycle status: unconfirmed.** The directory name is newer than
`book2025-2026/`, but no repository instruction establishes that it is the
active collection.

Verified source areas are:

- Grade 9 material directly under `grade9/`;
- Grade 10 Terms 1 and 3 under `grade10/`;
- Grade 11 Terms 2 and 3 under `grade11/`;
- olympiad, Cambridge, and diploma material under `olympiad/`; and
- year-local preambles, templates, graphs, and images under `preamble/`.

Many `.tex` files declare `\documentclass` and appear to be document entry
points; others are imported fragments or templates. The repository does not
identify a supported TeX distribution, engine, invocation directory, or
complete entry-point list. Therefore no canonical compile command is asserted.

## Independence and unresolved labels

Keep all imports, preambles, graphs, images, and activity datasets local to this
academic-year tree. Do not replace duplicated files with cross-year imports or
symlinks. Copy-forward and archive/backport policy remain unconfirmed; review
cross-year fixes explicitly rather than applying them automatically.

Several `G10_T2_*` filenames are currently located below
`grade10/term_1/`. Repository evidence does not establish whether this is a
curricular label or a placement error. They have deliberately not been moved or
renamed. The same rule applies to spelling, capitalization, and apparent grade
prefix anomalies until an owner confirms the intended identifiers and a
supported compilation workflow is available.

PDFs and compiler auxiliary files are ignored by the root `.gitignore`.
`clean-latex.bat` removes common generated files on Windows.
