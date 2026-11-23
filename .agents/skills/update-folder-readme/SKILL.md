---
name: update-folder-readme
description: Update a Global Economics directory summary by Markdown filename or filepath, or create one at an explicit missing filepath. Existing summaries use strictly newer sources; creation reviews all eligible immediate inputs.
---

# Update Folder README

Accept exactly one Markdown filename or filepath with a `.md` or `.markdown`
extension (case insensitive), for example:

```text
$update-folder-readme README-B_G11_T2_PA.md
$update-folder-readme template_README.md
$update-folder-readme "folder notes.md"
$update-folder-readme "teacher/assets/css/folder notes.markdown"
$update-folder-readme C:\Users\orlan\Desktop\SanBartolo\global_economics\teacher\assets\css\README_TAcss.md
$update-folder-readme \teacher\assets\css\README_TAcss.md
```

Accept Windows absolute and repository-relative paths with either slash style.
A single leading slash or backslash (including the example above) means
repository-relative. Relative paths are anchored to the Git root, not the
working directory. Reject extra arguments, non-Markdown names, control
characters, invalid portable path components, `..` traversal, drive-relative
paths, UNC paths, directories as targets, and symlink/junction traversal.
The resolved target must remain inside the repository and its parent must
already exist; never create parent directories. A quoted path or filename
containing spaces is one argument. Treat the
selected Markdown file as its directory's summary regardless of its name.
Recognized codes matching
`^README-(B|W)_G(10|11)_T(1|2|3)_(PA|CA|SL|LE|ER)\.md$`
provide optional context: B/W = Book/Webpage; G10/G11 = grades; T1–T3 = terms;
PA/CA/SL/LE/ER = Practice activity/Classroom activity/Slides/Learning
evidence/Extra resource. Never infer a path from codes. For other names derive
purpose from permitted source evidence and supported existing descriptions;
the filename alone is not evidence of substantive contents.

## Discover and review

Use `scripts/update_readme.py` relative to this skill directory. From anywhere
inside the repository, run:

```text
python <helper> prepare README-B_G11_T2_PA.md --state <temporary-state.json>
python <helper> prepare template_README.md --state <temporary-state.json>
python <helper> prepare "teacher/assets/css/folder notes.md" --state <temporary-state.json>
python <helper> prepare "\teacher\assets\css\README_TAcss.md" --state <temporary-state.json>
```

Keep state and the UTF-8 proposal outside the summarized folder, preferably
in the system temporary directory. The helper finds the Git root. Explicit
paths resolve directly, without repository-wide discovery: an existing file
selects update mode and a missing file selects creation mode. For a bare
filename only, find exact matches, including untracked files in normal content directories,
excluding Git internals, caches, build directories, and symlink traversal.
No match: report that an explicit filepath is required for creation and stop;
never guess a destination. Multiple matches: list
every repository-relative path and ask which to use; after the answer rerun
prepare with internal `--select <repository-relative-path>`. This resolves
ambiguity; `--select` is only for bare-filename discovery.
Report traversal errors rather than treating incomplete discovery as unique.

In update mode, prepare fixes the selected file's original filesystem `st_mtime_ns` cutoff before changes,
and records immediate file/folder metadata plus immediate child READMEs.
Only `mtime_ns > cutoff_ns` qualifies; equal times never qualify. Use integer
nanoseconds consistently and UTC when displaying them. Never substitute Git
dates, creation times, document dates, or now.

In creation mode, prepare records `target_existed: false`, `mode: create`,
`cutoff_ns: null`, and `cutoff_utc: "not applicable"`. There is no cutoff:
review all eligible immediate source files and qualifying immediate child
READMEs regardless of modification time. Apply the live exclusions and resolve
child-summary ambiguity before reading. Never recursively inspect subfolders.
Describe the planned summary's own purpose, commands, sections, and tree entry
from the proposal; it is not an existing input. Report unsupported, unreadable,
unreviewed, or incomplete inputs rather than guessing their contents.

Read the existing selected summary (update mode only) and live
`book2026-2027/preamble/template_README.md` as control documents regardless of
timestamps. If the live control template is missing, stop with a clear error;
never create it without its instructions, even when it is the explicit target.
Read sources through:

```text
python <helper> read --state <temporary-state.json> --path <repository-relative-path>
```

This gates reads to controls and the state's `eligible` paths and records
reviewed inputs. Apply the live template exclusions before reading sources,
including similar generated LaTeX artifacts; the helper screens known artifacts
but the live template remains authoritative. For eligible binary assets use
the helper's `--output <temporary-file>` option, then inspect that copy with
the appropriate viewer. Record unreadable/unsupported files as limitations.

In update mode, never reopen or hash unchanged source contents, force a full review, or use
the older README skill's cache workflow. Reuse existing descriptions, public
commands, and explicit section analyses for unchanged files. A newly discovered
older/equal file lacking an existing description is incomplete: report it
without inferring its contents from its name. Template changes and source
imports/links never authorize reading unchanged dependencies.

For subfolder descriptions read only eligible immediate child READMEs, using
the same cutoff in update mode and no cutoff in creation mode; resolve multiple
child README candidates before reading.
Child-summary discovery remains limited to `README.md` and `README-*.md`
(case sensitive), not arbitrary Markdown files. Accepting a nonstandard target
does not expand this rule.
Do not recursively review subfolders. Preserve supported existing descriptions
or report unavailable information when no qualifying child README is available.

## Compose and save

Build a complete proposal before writing. Follow the live template's exclusions,
concise English, type/name ordering, relative forward-slash links, tables, and
immediate directory tree. Preserve the standard composition:

```text
# Directory Summary
## Purpose
## Files
## Folders
## Directory Structure
## Public Commands
## Document Sections
```

Write descriptions useful to LLM agents navigating the repository. Where
permitted evidence supports it, explain each file's concrete purpose,
substantive contents, when an agent should consult it, and relevant public
commands or explicit document sections. Use precise, concise English, actual
filenames, and relative links. Avoid generic descriptions, unsupported
relationships, and guesses based only on filenames. Do not read unchanged
dependencies to enrich descriptions; reuse supported descriptions or report
missing information.

Create or update reviewed files' descriptions, public definitions (including aliases
and variants), and explicit sections in source order/hierarchy wherever
represented. In update mode, update purpose only when reviewed changes support it. Derive
the selected summary's own description/sections from the proposal, including
its actual name and role even if it is not called README. Reconcile names,
existence, links, removed items, and the target's actual filename from metadata
alone. Ensure Files, Folders, commands, sections, links, and tree agree; remove
excluded artifacts everywhere. When full template compliance requires unavailable
unchanged contents, preserve supported content and report the limitation.

### When the target is the live control template

For `book2026-2027/preamble/template_README.md`, treat control and target as
one record, review it once as a control, and exclude controls from the newer-source list.
The helper preserves the exact bytes before the first standalone
`# Directory Summary` line: the template title, AI instructions, exclusions,
ordering/link/table rules, and `## Output Template` heading. Keep this prefix
unchanged. If that boundary is missing, stop and report the malformed template.

Replace only the summary beginning at that boundary with the standard directory
summary and all six sections above, describing the template's own directory.
This is the explicit exception to the template's ordinary instruction to omit
AI rules and add no extra sections: normal summaries contain only the standard
summary; this dual-purpose file retains its control prefix followed by the
standard summary. Later runs must treat that summary as structural guidance,
replace its directory-specific rows with verified information, and omit the
prefix unless updating the template itself. Its self-description must explain
both roles, and its Document Sections row must include the preserved control
headings as well as the summary headings in actual order/hierarchy.

After checking the proposal, save only through:

```text
python <helper> commit --state <temporary-state.json> --proposal <proposal.md>
```

The helper checks controls, reviewed inputs, and inventory for concurrent
edits. In update mode it avoids writing identical bytes and otherwise replaces
the summary atomically. In creation mode it refuses a target that appeared
after prepare and publishes atomically without overwriting (Windows no-overwrite
rename; hard-link publication on POSIX). If the filesystem cannot support this,
stop; never fall back to an overwriting operation or a partial target write.
On conflict stop and report; never overwrite a stale proposal.
Only the selected summary may change. Do not modify sources, other summaries,
or unrelated skills; the live template may change only when it is the selected
target and its instruction prefix must remain intact. Never touch timestamps
or make cosmetic cutoff-advancing writes. Filesystem timestamps cannot detect edits preserving
or backdating modification times; this does not authorize hashing unchanged
sources.

## Completion report

Report `created`, `updated`, or `already current`; the repository-relative
target; the fixed update cutoff (UTC with nine fractional digits and exact epoch
nanoseconds), or “not applicable” for creation; reviewed source inputs and
controls; and limitations. Identify skipped, unsupported, unreadable, ambiguous,
conflicting, incomplete, and unreviewed eligible inputs. For updates, also
identify newly discovered older/equal files without prior information. The
helper reports unreviewed eligible inputs automatically; add review-specific
limitations in the completion message. If stopped before saving, say so explicitly.
