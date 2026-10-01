#!/usr/bin/env python3
"""Extract criterion attainment from academic-evaluation Excel exports.

The school's ``.xls`` reports are actually Excel-compatible HTML files.  This
module reads those files without third-party packages and also supports normal
``.xlsx`` workbooks.  Legacy binary ``.xls`` files can be read when ``xlrd`` is
installed.

Usage::

    python extract_results.py "original"
"""

from __future__ import annotations

import argparse
import csv
import importlib
import importlib.util
import json
import re
import sys
import zipfile
from collections import OrderedDict
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable, Sequence
from xml.etree import ElementTree as ET


CRITERIA = [f"C{i}" for i in range(1, 11)]
OUTPUT_COLUMNS = ["No.", "Student Name", *CRITERIA, "Total Periodo", "% Periodo"]
UNIFIED_OUTPUT_COLUMNS = ["No.", "Student Name", "Group", *CRITERIA,
                          "Total Periodo", "% Periodo"]
YES_WORDS = {"si", "sí", "yes", "y", "true", "1", "x", "alcanzado", "logrado"}
NO_WORDS = {"no", "n", "false", "0", "no alcanzado", "no logrado"}


@dataclass
class Cell:
    """A cell's displayed value and the metadata useful to the HTML parser."""

    value: str = ""
    attrs: dict[str, str] = field(default_factory=dict)

    @property
    def hidden(self) -> bool:
        style = re.sub(r"\s+", "", self.attrs.get("style", "").lower())
        return "display:none" in style


class _HTMLTableParser(HTMLParser):
    """Small, dependency-free parser for the Excel-compatible HTML exports."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[list[Cell]] = []
        self._row: list[Cell] | None = None
        self._cell: Cell | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag == "tr":
            self._row = []
        elif tag in {"td", "th"} and self._row is not None:
            self._cell = Cell(attrs={key.lower(): value or "" for key, value in attrs})

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.value += data

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"td", "th"} and self._cell is not None and self._row is not None:
            self._cell.value = _clean_text(self._cell.value)
            self._row.append(self._cell)
            self._cell = None
        elif tag == "tr" and self._row is not None:
            if self._row:
                self.rows.append(self._row)
            self._row = None


def _clean_text(value: object) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def _criterion_number(value: str) -> int | None:
    """Recognize C1, Criterio 1, and longer headers containing those labels."""
    text = _clean_text(value)
    match = re.search(r"(?i)(?:\bC|criterio\s*)0*(10|[1-9])\b", text)
    return int(match.group(1)) if match else None


def _read_html_excel(path: Path) -> list[list[Cell]]:
    raw = path.read_bytes()
    # Reports normally declare UTF-8 and may start with a BOM.  The fallbacks
    # make exports saved by older Spanish-language Excel versions usable too.
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    parser = _HTMLTableParser()
    parser.feed(text)
    return parser.rows


def _xlsx_strings(archive: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    return ["".join(node.itertext()) for node in root]


def _read_xlsx(path: Path) -> list[list[Cell]]:
    """Read the first worksheet of an xlsx using only the standard library."""
    with zipfile.ZipFile(path) as archive:
        strings = _xlsx_strings(archive)
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        relationships = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
        sheet = next(node for node in workbook.iter() if node.tag.endswith("}sheet"))
        rel_id = next(value for key, value in sheet.attrib.items() if key.endswith("}id"))
        target = relationships[rel_id].lstrip("/")
        sheet_path = target if target.startswith("xl/") else f"xl/{target}"
        root = ET.fromstring(archive.read(sheet_path))

        result: list[list[Cell]] = []
        for row_node in (node for node in root.iter() if node.tag.endswith("}row")):
            values: dict[int, str] = {}
            for node in row_node:
                if not node.tag.endswith("}c"):
                    continue
                reference = node.attrib.get("r", "A1")
                letters = re.match(r"[A-Z]+", reference.upper()).group(0)  # type: ignore[union-attr]
                column = 0
                for letter in letters:
                    column = column * 26 + ord(letter) - 64
                value_node = next((child for child in node if child.tag.endswith("}v")), None)
                inline = next((child for child in node if child.tag.endswith("}is")), None)
                value = "" if value_node is None else value_node.text or ""
                if node.attrib.get("t") == "s" and value:
                    value = strings[int(value)]
                elif inline is not None:
                    value = "".join(inline.itertext())
                values[column - 1] = _clean_text(value)
            width = max(values, default=-1) + 1
            result.append([Cell(values.get(index, "")) for index in range(width)])
        return result


def _read_binary_xls(path: Path) -> list[list[Cell]]:
    if importlib.util.find_spec("xlrd") is None:
        raise RuntimeError(
            "This is a binary .xls file. Install xlrd (`python -m pip install xlrd`) "
            "or save it as .xlsx. The supplied HTML-based .xls exports need no dependency."
        )
    xlrd = importlib.import_module("xlrd")
    sheet = xlrd.open_workbook(path).sheet_by_index(0)
    return [[Cell(_clean_text(sheet.cell_value(row, col))) for col in range(sheet.ncols)]
            for row in range(sheet.nrows)]


def read_source_file(path: Path) -> list[list[Cell]]:
    """Read HTML-.xls, OOXML-.xlsx, or (with xlrd) binary-.xls input."""
    if path.suffix.lower() not in {".xls", ".xlsx"}:
        raise ValueError("Input must have an .xls or .xlsx extension")
    signature = path.read_bytes()[:8]
    if signature.startswith(b"PK"):
        return _read_xlsx(path)
    if signature.startswith((b"<", b"\xef\xbb\xbf<")):
        return _read_html_excel(path)
    return _read_binary_xls(path)


def _find_layout(rows: Sequence[Sequence[Cell]]) -> tuple[int, int, list[int]]:
    """Return header row, student column, and physical criterion columns.

    Rectangular workbooks map criterion headers directly.  The supplied HTML
    reports insert hidden evidence-separator cells only in body rows; those are
    deliberately handled later by their visible-cell order.
    """
    best: tuple[int, int, list[int]] | None = None
    for row_index, row in enumerate(rows):
        mapping: dict[int, int] = {}
        student_column = -1
        for column, cell in enumerate(row):
            number = _criterion_number(cell.value)
            if number is not None:
                mapping[number] = column
            if re.search(r"(?i)\b(estudiantes?|students?|alumnos?|nombres?)\b", cell.value):
                student_column = column
        if len(mapping) >= 2:
            columns = [mapping.get(number, -1) for number in range(1, 11)]
            candidate = (row_index, student_column, columns)
            if best is None or len(mapping) > sum(c >= 0 for c in best[2]):
                best = candidate
    if best is None:
        raise ValueError("Could not find a header row containing criterion labels C1-C10")
    header_row, student_column, columns = best
    if student_column < 0:
        # In two-tier headers ESTUDIANTES is commonly in the preceding row.
        for index in range(header_row, -1, -1):
            for column, cell in enumerate(rows[index]):
                if re.search(r"(?i)\b(estudiantes?|students?|alumnos?|nombres?)\b", cell.value):
                    student_column = column
                    break
            if student_column >= 0:
                break
    if student_column < 0:
        raise ValueError("Could not identify the student-name column")
    return header_row, student_column, columns


def _attainment(value: str) -> str:
    normalized = _clean_text(value).casefold()
    if normalized in YES_WORDS:
        return "Yes"
    if normalized in NO_WORDS:
        return "No"
    return ""


def extract_students(rows: Sequence[Sequence[Cell]]) -> list[dict[str, str]]:
    """Extract and de-duplicate students, combining split/repeated rows."""
    header_row, student_column, criterion_columns = _find_layout(rows)
    students: OrderedDict[str, dict[str, str]] = OrderedDict()
    current_name = ""

    for row in rows[header_row + 1:]:
        if student_column >= len(row):
            continue
        name_cell = row[student_column]
        # The HTML report's displayed cell includes dropdown help text; title
        # contains exactly the displayed student name before that decoration.
        if any(cell.hidden for cell in row):
            visible_after_name = [cell for cell in row[student_column + 1:] if not cell.hidden]
            criterion_cells = visible_after_name[:10]
        else:
            criterion_cells = [row[column] if 0 <= column < len(row) else Cell()
                               for column in criterion_columns]

        name = _clean_text(name_cell.attrs.get("title") or name_cell.value)
        if name and not re.fullmatch(r"\d+(?:\.0+)?", name):
            current_name = name
        elif current_name and any(_attainment(cell.value) for cell in criterion_cells):
            # A blank name commonly means that Excel merged the student's name
            # vertically across several criterion rows.
            name = current_name
        else:
            continue

        record = students.setdefault(name, {criterion: "" for criterion in CRITERIA})

        for criterion, cell in zip(CRITERIA, criterion_cells):
            result = _attainment(cell.value)
            # On repeated rows, an attained observation wins; otherwise retain
            # an evaluated No over a missing value.
            if result == "Yes" or (result == "No" and not record[criterion]):
                record[criterion] = result

    if not students:
        raise ValueError("No student records were found below the criterion header")
    return [{"Student Name": name, **criteria} for name, criteria in students.items()]


def extract_criteria(rows: Sequence[Sequence[Cell]]) -> list[dict[str, str]]:
    """Public extraction stage retained separately for reuse and testing."""
    return extract_students(rows)


def calculate_period_results(students: Iterable[dict[str, str]]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for number, student in enumerate(students, 1):
        yes_count = sum(student[criterion] == "Yes" for criterion in CRITERIA)
        evaluated = sum(student[criterion] in {"Yes", "No"} for criterion in CRITERIA)
        percentage = "" if evaluated == 0 else f"{yes_count / evaluated:.0%}"
        results.append({"No.": number, **student, "Total Periodo": yes_count,
                        "% Periodo": percentage})
    return results


def export_csv(
    rows: Iterable[dict[str, object]],
    output_path: Path,
    columns: Sequence[str] = OUTPUT_COLUMNS,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_csv_manifest(output_folder: Path) -> None:
    """Index generated CSVs so a static browser page can discover their names."""
    files = sorted(
        (path.name for path in output_folder.iterdir()
         if path.is_file() and path.suffix.casefold() == ".csv"),
        key=lambda name: (name.casefold(), name),
    )
    manifest = output_folder / "csv-manifest.json"
    manifest.write_text(
        json.dumps({"files": files}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def output_folder_for(input_folder: Path) -> Path:
    """Return the sibling folder used for all generated CSV files."""
    if input_folder.name.casefold() == "original":
        return input_folder.with_name("Extracted")
    return input_folder.with_name(f"{input_folder.name}-Extracted")


def find_excel_files(input_folder: Path) -> list[Path]:
    """Find supported, non-temporary Excel files directly in a folder."""
    return sorted(
        (
            path for path in input_folder.iterdir()
            if path.is_file()
            and path.suffix.casefold() in {".xls", ".xlsx"}
            and not path.name.startswith("~$")
        ),
        key=lambda path: (path.name.casefold(), path.name),
    )


def individual_output_paths(
    files: Sequence[Path], output_folder: Path
) -> dict[Path, Path]:
    """Create readable output names without collisions between equal stems."""
    stem_counts: dict[str, int] = {}
    for path in files:
        key = path.stem.casefold()
        stem_counts[key] = stem_counts.get(key, 0) + 1

    return {
        path: output_folder / (
            f"{path.stem}.csv"
            if stem_counts[path.stem.casefold()] == 1
            and path.stem.casefold() != "unified_extracted"
            else f"{path.stem}_{path.suffix.lstrip('.')}.csv"
        )
        for path in files
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="folder containing .xls or .xlsx files")
    args = parser.parse_args(argv)

    input_folder = args.input
    if not input_folder.exists():
        parser.error(f"input folder does not exist: {input_folder}")
    if not input_folder.is_dir():
        parser.error(f"input path is not a directory: {input_folder}")

    try:
        files = find_excel_files(input_folder)
    except OSError as exc:
        parser.exit(1, f"error: could not scan input folder {input_folder}: {exc}\n")
    if not files:
        parser.error(f"no supported Excel files found in: {input_folder}")

    output_folder = output_folder_for(input_folder)
    output_paths = individual_output_paths(files, output_folder)
    unified_rows: list[dict[str, object]] = []
    failures = 0
    try:
        output_folder.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        parser.exit(1, f"error: could not create output folder {output_folder}: {exc}\n")

    for source in files:
        try:
            source_rows = read_source_file(source)
            students = extract_criteria(source_rows)
            results = calculate_period_results(students)
            output = output_paths[source]
            export_csv(results, output)
        except (OSError, ValueError, RuntimeError, zipfile.BadZipFile, ET.ParseError) as exc:
            failures += 1
            print(f"error: could not process {source.name}: {exc}", file=sys.stderr)
            continue

        group = source.stem.split("_", 1)[0]
        unified_rows.extend({**result, "Group": group} for result in results)
        print(f"Extracted {len(results)} students from {source.name} to {output}")

    if unified_rows:
        unified_output = output_folder / "Unified_Extracted.csv"
        try:
            export_csv(unified_rows, unified_output, UNIFIED_OUTPUT_COLUMNS)
        except OSError as exc:
            parser.exit(1, f"error: could not write {unified_output}: {exc}\n")
        print(f"Combined {len(unified_rows)} students into {unified_output}")
    else:
        print("error: no Excel files could be processed", file=sys.stderr)

    try:
        write_csv_manifest(output_folder)
    except OSError as exc:
        parser.exit(1, f"error: could not write CSV manifest: {exc}\n")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
