# Assessment Results Normalizer

`results.py` extracts four-row student records from irregular `.xls` or `.xlsx`
exports, normalizes C1–C10 values, and prints per-file summaries.

## Data handling

The adjacent workbooks are externally supplied inputs and may contain
student-level information. Their provenance, retention period, and authorization
for relocation are not documented in this repository. Do not commit derived
output, quote workbook contents in issues/logs, or move/delete the workbooks
without explicit authorization. For that reason, code and inputs remain in
their existing dated directory.

## Runtime requirements

- Python 3
- `pandas`
- an Excel reader compatible with the input format (`xlrd` for legacy `.xls`;
  `openpyxl` may be needed for `.xlsx`)
- `tabulate` is optional; the script falls back to pandas text output

No exact dependency versions are pinned because a clean compatible environment
has not yet been verified in repository instructions. Install dependencies in a
local virtual environment rather than globally, for example:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install pandas xlrd openpyxl
```

The default command processes `10A.xls`; `--all` processes every adjacent Excel
input. These commands can reveal student data, so run them only in an authorized
local environment and do not capture their output in shared logs:

```bash
python teacher/tools/2026-02-19-results/results.py --help
python teacher/tools/2026-02-19-results/results.py --file 10A.xls
python teacher/tools/2026-02-19-results/results.py --all
```

The CLI imports pandas before parsing `--help`, so even the help command requires
the core dependency to be installed.
