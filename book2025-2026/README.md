# 2025–2026 LaTeX Collection

## Status and contents

**Lifecycle status: unconfirmed.** No repository instruction identifies this
tree as active or archived.

Verified source areas are:

- Grade 9 material directly under `grade9/`;
- Grade 10 Terms 2 and 3 under `grade10/`;
- Grade 11 Terms 2 and 3 under `grade11/`;
- olympiad material under `olympiad/`; and
- year-local preambles, templates, graphs, and images under `preamble/`.

Many `.tex` files declare `\documentclass` and appear to be document entry
points; others are imported fragments or templates. The repository does not
identify a supported TeX distribution, engine, invocation directory, or
complete entry-point list. Therefore no canonical compile command is asserted.

## Independence and copy-forward policy

Keep all imports, preambles, graphs, images, and activity datasets local to this
academic-year tree. Do not replace duplicated files with cross-year imports or
symlinks. The substantial byte-identical overlap with `book2026-2027/` is
consistent with copy-forward, but no repository evidence establishes an archive
date or a rule for backporting fixes.

Until an owner defines that policy:

- do not assume a fix in one year should or should not be copied to the other;
- review each cross-year correction explicitly; and
- do not rename files solely to normalize spelling or capitalization.

PDFs and compiler auxiliary files are ignored by the root `.gitignore`.
`clean-latex.bat` removes common generated files on Windows.
