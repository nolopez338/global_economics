#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

CRITERIA = [f"C{i}" for i in range(1, 11)]


def list_xls_files(folder: Path) -> List[Path]:
    """Return sorted .xls files in a folder."""
    return sorted(p for p in folder.glob("*.xls") if p.is_file())


def read_raw_xls(path: Path) -> pd.DataFrame:
    """Read a legacy .xls file into a raw DataFrame without assuming headers."""
    try:
        return pd.read_excel(path, header=None, dtype=object, engine="xlrd")
    except ImportError:
        print(
            "Error: Missing Excel engine for .xls files.\n"
            "Please install xlrd with:\n"
            "  pip install xlrd==1.2.0",
            file=sys.stderr,
        )
        raise SystemExit(1)
    except Exception as exc:
        msg = str(exc).lower()
        if "xlrd" in msg or "engine" in msg or "xls" in msg:
            print(
                f"Error reading '{path.name}': {exc}\n"
                "Tip: ensure xlrd is installed and compatible with .xls:\n"
                "  pip install xlrd==1.2.0",
                file=sys.stderr,
            )
            raise SystemExit(1)
        raise


def _normalize_space_upper(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    text = str(value).strip()
    return " ".join(text.split()).upper()


def _normalize_yes_no(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    text = str(value).strip()
    if not text:
        return ""
    upper = text.upper().replace("Í", "I")
    if upper == "SI":
        return "Si"
    if upper == "NO":
        return "No"
    return ""


def _first_non_empty(values: List[Any]) -> Any:
    for val in values:
        if pd.isna(val):
            continue
        if str(val).strip() != "":
            return val
    return ""


def detect_columns(df_raw: pd.DataFrame, debug: bool = False) -> Dict[str, Any]:
    """Detect row/column positions for No, ESTUDIANTES, and C1..C10 headers."""
    header_row_idx = None
    c1_col_idx = None

    for ridx in range(df_raw.shape[0]):
        row = df_raw.iloc[ridx]
        for cidx, val in enumerate(row.tolist()):
            if _normalize_space_upper(val) == "C1":
                header_row_idx = ridx
                c1_col_idx = cidx
                break
        if header_row_idx is not None:
            break

    if header_row_idx is None:
        raise ValueError("Could not detect criteria header row (missing C1).")

    search_start = max(0, header_row_idx - 3)
    search_end = min(df_raw.shape[0], header_row_idx + 1)

    no_col_idx = None
    students_col_idx = None

    for ridx in range(search_start, search_end):
        row = df_raw.iloc[ridx]
        for cidx, val in enumerate(row.tolist()):
            token = _normalize_space_upper(val)
            if token == "NO" and no_col_idx is None:
                no_col_idx = cidx
            elif token == "ESTUDIANTES" and students_col_idx is None:
                students_col_idx = cidx

    c_cols: Dict[str, int] = {}
    header_row = df_raw.iloc[header_row_idx]
    norm_header = [_normalize_space_upper(v) for v in header_row.tolist()]

    for ck in CRITERIA:
        token = ck.upper()
        if token in norm_header:
            c_cols[ck] = norm_header.index(token)

    if no_col_idx is None:
        raise ValueError("Could not detect 'No' column.")
    if students_col_idx is None:
        raise ValueError("Could not detect 'ESTUDIANTES' column.")

    missing = [ck for ck in CRITERIA if ck not in c_cols]
    if missing:
        raise ValueError(f"Missing criteria columns: {', '.join(missing)}")

    meta = {
        "criteria_header_row": header_row_idx,
        "data_start_row": header_row_idx + 1,
        "col_no": no_col_idx,
        "col_students": students_col_idx,
        "col_criteria": c_cols,
    }

    if debug:
        print("[DEBUG] Header detection:")
        print(f"  criteria_header_row={meta['criteria_header_row']} (0-indexed)")
        print(f"  data_start_row={meta['data_start_row']} (0-indexed)")
        print(f"  col_no={meta['col_no']}")
        print(f"  col_students={meta['col_students']}")
        print(f"  col_criteria={meta['col_criteria']}")

    return meta


def extract_records(df_raw: pd.DataFrame, meta: Dict[str, Any]) -> pd.DataFrame:
    """Extract one clean row per student from 4-row chunks."""
    records: List[Dict[str, Any]] = []
    start = int(meta["data_start_row"])
    col_no = int(meta["col_no"])
    col_students = int(meta["col_students"])
    col_criteria: Dict[str, int] = meta["col_criteria"]

    nrows = df_raw.shape[0]
    for chunk_start in range(start, nrows, 4):
        chunk_end = min(chunk_start + 4, nrows)
        chunk = df_raw.iloc[chunk_start:chunk_end]
        if chunk.empty:
            continue

        no_val = _first_non_empty(chunk.iloc[:, col_no].tolist())
        student_val = _first_non_empty(chunk.iloc[:, col_students].tolist())

        if str(student_val).strip() == "" and str(no_val).strip() == "":
            continue

        row: Dict[str, Any] = {
            "No": "" if pd.isna(no_val) else str(no_val).strip(),
            "ESTUDIANTES": "" if pd.isna(student_val) else str(student_val).strip(),
        }

        for ck in CRITERIA:
            col_idx = col_criteria[ck]
            val = _first_non_empty(chunk.iloc[:, col_idx].tolist())
            row[ck] = _normalize_yes_no(val)

        records.append(row)

    columns = ["No", "ESTUDIANTES", *CRITERIA]
    return pd.DataFrame(records, columns=columns)


def print_table(df_clean: pd.DataFrame) -> None:
    """Print table using tabulate if available, otherwise pandas fallback."""
    if df_clean.empty:
        print("(No student records found)")
        return

    try:
        from tabulate import tabulate  # type: ignore

        print(tabulate(df_clean, headers="keys", tablefmt="grid", showindex=False))
    except Exception:
        print(df_clean.to_string(index=False))


def print_summary(df_clean: pd.DataFrame) -> None:
    """Print total students and per-criterion Si/No/empty counts."""
    total = len(df_clean)
    print("\nSummary")
    print(f"- total students: {total}")

    for ck in CRITERIA:
        series = df_clean[ck] if ck in df_clean.columns else pd.Series(dtype=object)
        yes = int((series == "Si").sum())
        no = int((series == "No").sum())
        empty = int((series == "").sum())
        print(f"- {ck}: Si={yes}, No={no}, empty={empty}")


def _process_file(path: Path, debug: bool = False) -> None:
    print(f"\n=== {path.name} ===")
    df_raw = read_raw_xls(path)
    meta = detect_columns(df_raw, debug=debug)
    df_clean = extract_records(df_raw, meta)
    print_table(df_clean)
    print_summary(df_clean)


def main() -> None:
    folder = Path(__file__).resolve().parent

    parser = argparse.ArgumentParser(description="Extract 4-row student records from irregular .xls files.")
    parser.add_argument("--file", type=str, default="10A.xls", help="Single .xls file to process (default: 10A.xls)")
    parser.add_argument("--all", action="store_true", help="Process all .xls files in this folder")
    parser.add_argument("--debug", action="store_true", help="Print debug info for detected headers/columns")

    args = parser.parse_args()

    xls_files = list_xls_files(folder)
    if not xls_files:
        print(f"No .xls files found in: {folder}", file=sys.stderr)
        raise SystemExit(1)

    if args.all:
        for p in xls_files:
            _process_file(p, debug=args.debug)
        return

    target = folder / args.file
    if not target.exists():
        print(f"Error: File not found: {target.name}", file=sys.stderr)
        print("Available .xls files:", file=sys.stderr)
        for p in xls_files:
            print(f"- {p.name}", file=sys.stderr)
        raise SystemExit(1)

    _process_file(target, debug=args.debug)


if __name__ == "__main__":
    main()
