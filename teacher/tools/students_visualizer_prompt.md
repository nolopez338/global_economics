# Student visualizer practice-mode implementation prompt

Use the following prompt when requesting future work on practice-mode name
matching:

> Update `teacher/tools/students_visualizer.html` so Practice Mode reliably
> compares the typed answer with the name encoded by the displayed picture's
> filename. Keep filename parsing and answer matching in
> `teacher/tools/assets/js/student-name-matcher.js`, with Node-runnable tests in
> `teacher/tools/tests/student-name-matcher.test.js`. A filename has the form
> `Group-Full Name.png`; remove only the group prefix and extension. Treat case,
> repeated whitespace, punctuation separators, and diacritics as insignificant.
> Accept one or more **complete** name components in any order, including the
> full name, but reject empty answers, substrings, unknown components, and reuse
> of a component that occurs only once. The result must always be checked
> against the same student whose image is currently displayed. Preserve the
> read-only File System Access workflow, current group/search filters, keyboard
> submission, and correct/error feedback. Add regression cases for first-name,
> full-name, reordered-name, accent-insensitive, substring, empty, unknown, and
> duplicate-token answers, then run the test directly with Node.

## Acceptance check

```bash
node teacher/tools/tests/student-name-matcher.test.js
```
