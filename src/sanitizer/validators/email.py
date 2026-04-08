# src/sanitizer/validators/email.py

from re import match

from sanitizer.models import Row, ValidationResult


class EmailValidator:
    def __init__(self, column: str) -> None:
        self.column = column

    def validate(self, row: Row) -> ValidationResult:
        value = row.data[self.column]
        rejection_reason = f"invalid:{self.column}"
        if not value:
            return ValidationResult(is_valid=False, rejection_reason=rejection_reason)

        if match(r"^[^@\s]+@[^@\s]+\.[^@\s]+", value):
            return ValidationResult(is_valid=True)
        return ValidationResult(is_valid=False, rejection_reason=rejection_reason)
