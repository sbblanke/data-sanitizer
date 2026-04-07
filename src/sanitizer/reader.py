# reader.py

import csv
import sys

from sanitizer.models import Config, Row


def _open_csv(path: str) -> list[dict]:
    for encoding in ("utf-8", "latin-1"):
        try:
            with open(path, "r", encoding=encoding) as f:
                return list(csv.DictReader(f))
        except UnicodeDecodeError:
            continue
    sys.exit(f"Error: could not decode file: {path}")


def read_csv(path: str, config: Config) -> list[Row]:
    try:
        rows = _open_csv(path)
    except FileNotFoundError:
        sys.exit(f"Error: file not found: {path}")

    if not rows:
        sys.exit("Error: CSV file is empty")

    headers = rows[0].keys()

    missing = []

    if config.primary_key not in headers:
        sys.exit(
            f"ERROR: primary key '{config.primary_key}' not found. Available columns: {list(headers)}"
        )
    for col in config.mandatory_columns:
        if col not in headers:
            missing.append(col)

    if missing:
        sys.exit(
            f"ERROR: The following columns are missing from the csv: {missing}. Available columns: {list(headers)}"
        )

    result = []
    for line_number, data in enumerate(rows, start=1):
        result.append(Row(data=data, line_number=line_number))

    return result
