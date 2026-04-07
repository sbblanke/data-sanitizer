# writer.py

import csv
import logging

from sanitizer.models import Row


def write_clean_csv(path: str, rows: list[Row]) -> None:
    if not rows:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].data.keys())
        writer.writeheader()
        for row in rows:
            writer.writerow(row.data)


def write_rejected_csv(path: str, rejected: list[tuple[Row, str]]) -> None:
    if not rejected:
        return
    fieldnames = list(rejected[0][0].data.keys()) + ["rejection_reason"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row, reason in rejected:
            writer.writerow({**row.data, "rejection_reason": reason})


def setup_audit_log(path: str) -> None:
    logging.basicConfig(
        filename=path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
