# src/sanitizer/pipeline.py

from sanitizer.duplicate import DuplicateChecker
from sanitizer.models import Row, SanitizeResult
import logging


class Pipeline:
    def __init__(self, duplicate_checker: DuplicateChecker, validators: list) -> None:
        self.duplicate_checker = duplicate_checker
        self.validators = validators

    def run(self, rows: list[Row]) -> SanitizeResult:
        cleaned: list[Row] = []
        rejected: list[tuple[Row, str]] = []
        duplicate_count = 0
        invalid_count = 0

        for row in rows:
            result = self.duplicate_checker.check(row)
            if not result.is_valid:
                rejected.append((row, result.rejection_reason))
                duplicate_count += 1
                logging.info(
                    f"Row {row.line_number} rejected: {result.rejection_reason}"
                )
                continue

            all_valid = True
            for v in self.validators:
                result = v.validate(row)
                if not result.is_valid:
                    all_valid = False
                    rejected.append((row, result.rejection_reason))
                    invalid_count += 1
                    logging.info(
                        f"Row {row.line_number} rejected: {result.rejection_reason}"
                    )
                    break
            if all_valid:
                cleaned.append(row)

        return SanitizeResult(
            cleaned_rows=cleaned,
            rejected_rows=rejected,
            total_input=len(rows),
            duplicate_count=duplicate_count,
            invalid_count=invalid_count,
        )
