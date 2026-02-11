from pathlib import Path
import csv
import json

REQUIRED_COLUMNS = [
    "Grade",
    "Section",
    "Class #",
    "Date",
    "Weekday",
    "Day",
    "Description",
    "Material",
    "Summary",
]


def load_schedule(csv_path: Path) -> list[dict]:
    with csv_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or missing a header row.")

        missing_columns = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
        if missing_columns:
            raise ValueError(
                "Missing required columns: " + ", ".join(missing_columns)
            )

        rows = []
        for row_number, row in enumerate(reader, start=2):
            try:
                grade = int(row["Grade"])
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid Grade at row {row_number}: {row['Grade']!r}. Must be an integer."
                ) from exc

            try:
                day = int(row["Day"])
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid Day at row {row_number}: {row['Day']!r}. Must be an integer."
                ) from exc

            normalized_row = {
                "Grade": grade,
                "Section": row["Section"],
                "Class #": row["Class #"],
                "Date": row["Date"],
                "Weekday": row["Weekday"],
                "Day": day,
                "Description": row["Description"],
                "Material": row["Material"],
                "Summary": row["Summary"],
            }
            rows.append(normalized_row)

    rows.sort(
        key=lambda item: (
            item["Grade"],
            item["Section"],
            item["Date"].replace("/", "-"),
            item["Class #"],
        )
    )
    return rows


def write_schedule_js(output_path: Path, rows: list[dict]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    json_content = json.dumps(rows, indent=2, ensure_ascii=False)

    file_content = "\n".join(
        [
            "// AUTO-GENERATED FILE",
            "// Generated from teacher/authoring/schedule.csv",
            "// Do not edit manually.",
            f"window.SCHEDULE_DATA = {json_content};",
            "",
        ]
    )

    output_path.write_text(file_content, encoding="utf-8")


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent

    csv_path = script_dir / "schedule.csv"
    output_path = project_root / "teacher" / "assets" / "js" / "schedule-data.js"

    try:
        rows = load_schedule(csv_path)
        write_schedule_js(output_path, rows)
    except ValueError as error:
        print(f"Error: {error}")
        raise SystemExit(1)

    print("schedule-data.js successfully generated.")


if __name__ == "__main__":
    main()
