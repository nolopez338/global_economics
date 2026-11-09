# 2026–2027 LaTeX Collection

## Status and contents

**Lifecycle status: unconfirmed.** The directory name is newer than
`book2025-2026/`, but no repository instruction establishes that it is the
active collection.

Verified source areas are:

- Grade 9 material directly under `grade9/`;
- Grade 10 Terms 1 and 3 under `grade10/`;
- Grade 11 Terms 2 and 3 under `grade11/`;
- olympiad, Cambridge, and diploma material under `olympiad/`;
- year-local preambles, graphs, and images under `preamble/`.

Many `.tex` files declare `\documentclass` and appear to be document entry
points; others are imported fragments or templates. The repository does not
identify a supported TeX distribution, engine, invocation directory, or
complete entry-point list. Therefore no canonical compile command is asserted.

## Authoring skills

Each skill links to its own guide, LaTeX scaffold, and build instructions.

- [Exam](../.agents/skills/global-economics-exam/SKILL.md) for student assessments with objectives, criteria, scores, and answer space.
- [Exam Solution](../.agents/skills/global-economics-exam-solution/SKILL.md) for worked scoring keys that follow the source exam.
- [Home Practice Activities](../.agents/skills/global-economics-home-practice/SKILL.md) for independent, criterion-linked work, including activities delivered on paper.
- [Print Handout](../.agents/skills/global-economics-print/SKILL.md) for numbered problem contexts followed by a characterization table.

The [recursive Windows build](compile_all_tex.bat) runs `latexmk -pdf` from
each source directory and explicitly includes the four skill scaffolds.

## Independence and unresolved labels

Keep all imports, preambles, graphs, images, and activity datasets local to this
academic-year tree. Do not replace duplicated files with cross-year imports or
symlinks. Copy-forward and archive/backport policy remain unconfirmed; review
cross-year fixes explicitly rather than applying them automatically.

Grade 10 Term 1 sources below `grade10/term_1/` use the confirmed
`G10_T1_*` identifier. Spelling, capitalization, and apparent grade-prefix
anomalies outside this authorized term migration remain unchanged pending an
owner decision and a supported compilation workflow.

The root `.gitignore` excludes common LaTeX auxiliary files.
`clean-latex.bat` removes common generated files on Windows.
