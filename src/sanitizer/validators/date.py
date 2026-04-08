# src/sanitizer/validators/date.py

from datetime import datetime

from sanitizer.models import Row, ValidationResult


class DateValidator:
    def __init__(self, column: str, date_format: str) -> None:
        self.column = column
        self.date_format = date_format

    def validate(self, row: Row) -> ValidationResult:
        value = row.data[self.column]
        rejection_reason = f"invalid:{self.column}"
        if not value:
            return ValidationResult(is_valid=False, rejection_reason=rejection_reason)

        try:
            datetime.strptime(value, self.date_format)
            return ValidationResult(is_valid=True)
        except ValueError:
            return ValidationResult(is_valid=False, rejection_reason=rejection_reason)
