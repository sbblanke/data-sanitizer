# src/sanitizer/duplicate.py

from sanitizer.models import Row, ValidationResult


class DuplicateChecker:
    def __init__(self, key_column: str) -> None:
        self.key_column = key_column
        self._seen = set()

    def check(self, row: Row) -> ValidationResult:
        value = row.data[self.key_column]
        rejection_reason = f"duplicate:{self.key_column}"
        if value in self._seen:
            return ValidationResult(is_valid=False, rejection_reason=rejection_reason)
        self._seen.add(value)
        return ValidationResult(is_valid=True)

    def reset(self) -> None:
        self._seen = set()
