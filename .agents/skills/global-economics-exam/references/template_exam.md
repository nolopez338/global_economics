# LaTeX and Build Guide

## Shared inputs and logo

Copy the [scaffold](../assets/template_exam.tex) into the exam source directory. It loads the [shared exam preamble](../../../../book/preamble/preamble_exams.tex) once. The preamble supplies the document class, packages, and [exam layout commands](../../../../book/preamble/preamble_exam_layout.tex).

The scaffold searches the shared preamble from its asset directory and from standard locations under the book directory. From another directory, add the absolute path to the shared preamble directory to `TEXINPUTS` for the build session. This resolves the initial preamble, its nested inputs, and graph imports. Use forward slashes in paths passed to TeX, a trailing slash on the directory, and an empty search component for TeX's default paths. PowerShell uses a semicolon as the separator.

~~~powershell
$env:TEXINPUTS = 'C:/path/to/repo/book/preamble/;'
~~~

The scaffold sets `\graphicspath` after the preamble to locate the [institutional logo](../../../../book/preamble/logo.png). For an external exam directory, TeX can also find the logo via `TEXINPUTS`. To specify a graphics directory explicitly, add it as a braced entry in `\graphicspath`, with a trailing slash. Add any exam-specific graphics directories there as well.

## Full-width front matter

Use `\ExamHeader{grade}{evidence number}{title}{term}` when the shared designation, teacher, and school year match the brief. The macro adds “Grade,” “Learning Evidence,” and “TERM” around its arguments.

For a named assessment without an evidence number, or when the metadata differs, replace the header call with a local adaptation of the shared three-cell layout. This block uses the same widths and helpers. Omit inapplicable metadata lines.

~~~latex
\noindent
\begin{tabularx}{\textwidth}{|C{2.8cm}|C{\dimexpr\textwidth-5.6cm-6\tabcolsep-4\arrayrulewidth\relax}|C{2.8cm}|}
  \hline
  \centering\vspace{3mm}\includegraphics[width=2.5cm]{logo.png}
  &
  \CellCenter{%
    \vspace{-5mm}
    \textbf{GLOBAL ECONOMICS}\par
    \textbf{Grade [grade] -- [assessment designation]}\par
    \textbf{[Exam title]}\par
    \textbf{[Teacher line]}%
  }
  &
  \CellCenter{\textbf{[Term]}\par\textbf{[School year]}}
  \\
  \hline
\end{tabularx}\par
~~~

Follow with `\LearningObjective{objective}{criteria}`, separating criterion entries with `\par`. Adjust the objective column's share with `\setYColumnWidth{fraction}` if needed. Place `\StudentInfo` below the objective when students identify their printed copy. Keep all three elements outside `multicols`.

## Two-column body

- Start with `\SubsectionBox*{Criteria assessment}`. Use the unstarred `\SubsectionBox` for questions and pass titles without numbers. The scaffold locally replaces the shared heading renderer while retaining its counter and starred interface; numbering continues across columns and pages. Its node already accounts for padding: do not subtract it again at calls.
- Use `\score{[criterion ID]-\sml{[points]}}` in the question heading. Within the same `\score` argument, list multiple criterion marks separated by `\quad`. Use the inline `\sscore` for separately scored tasks. If several tasks assess the same criterion, sum those task marks for the heading.
- Keep the matrix at a readable size within `\linewidth`. Add a row per question, a column per criterion, and a total row. Use a dash where a question assigns no points to a criterion. For a wide matrix, repeat the scaffold's table in blocks with descriptive labels such as “Available points (1 of 2).” Repeat the question-number column and rows in each block, with a total for each criterion shown there. Keep each label and table together. If a block is too tall for a column, split its rows into labeled question ranges, repeat the column headings, and show the criterion totals at the end of that block's final range.
- Size inline figures and tables to `\linewidth` and keep them with the relevant prompt. Use `\includegraphics[width=\linewidth]{...}` for an image or `tabularx` with `\linewidth` and wrapping cells for a text-heavy table. Check plot labels after sizing.
- Keep short questions and their workspace together in a `minipage` of width `\linewidth`. Let long questions flow across columns or pages, with breaks between tasks. Keep the heading with the opening prompt and group individual figures or answer areas with their tasks. For requested or on-exam response guides, read [response_guides.md](response_guides.md) and use the scaffold's empty response helpers.

## Neutral structural helpers

The scaffold adapts only the classroom-activity heading and response-box styles, locally to the exam; it does not change shared preambles. `\SubsectionBox` is the centered large bold black question/section level, with compact `black!10` fill, black .2 pt border, 2 mm corners and 3 pt padding. `\ExamTaskHeading{label and title}` supplies a left-aligned bold task level with `black!5` fill, no border, the same corners and padding. `\ExamSubtaskHeading{label and short title}` is plain bold underlined black text. Use only levels needed by the assessment, preserve task letters and separately scored subparts, and keep long underlined labels short enough to fit. Wrapped shaded headings respect local `\linewidth`; reserve extra opening-block height with `\Needspace` where necessary.

Keep concepts, notation, values and mathematics plain, without semantic colors, mathematical highlights or highlight legends. Inspect inherited macros and nested inputs before reuse; unwrap highlight-producing commands without removing substantive content. These permissions concern structural headings and empty response areas only, not classroom-activity counts, worked examples, teaching steps or its table families. Response tables have their own vertical-divider-only style in the response-guide reference; given-data and score tables retain their appropriate rules.

## Graphs

Use the [shared graph index](../../../../book/preamble/graphs/README-graphs.md) to find a suitable command for supplied figures. Read the macro definition to verify its argument order, widths, required libraries, and helper commands. After loading the exam preamble, import only the graph files the exam uses, including dependencies confirmed in those definitions. Use `\input{graphs/<file>.tex}` with the shared preamble directory on the input search path, or give the input an explicit path. Check the resulting graph against the task data and the current column width. For student graph responses, use blank axes and a light grid with a suitable uniform numerical scale as specified in the response-guide reference; do not reuse a helper that reveals derived support values or plotted results.

## Build and inspect

Run pdfLaTeX from the exam source directory. For a scaffold-only check, run it from `assets/` with `template_exam.tex`. Set the shared input path first when building outside the scaffold's search locations. To collect build files separately, pass an existing absolute directory via `-output-directory`. That option redirects generated files while the working directory still determines relative source paths.

~~~powershell
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="C:/path/to/build" exam.tex
~~~

Build twice to resolve question references. Check the log for missing inputs and overfull boxes. Open the PDF or render its pages to verify the actual layout, heading hierarchy, neutral box appearance, and absence of semantic highlights. When response guides are included, also perform the coverage and layout checks in the response-guide reference.
