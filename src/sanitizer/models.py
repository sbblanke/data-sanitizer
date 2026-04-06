# models.py

from dataclasses import dataclass


@dataclass(frozen=True)
class Row:
    data: dict[str, str]
    line_number: int


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    rejection_reason: str = ""


@dataclass(frozen=True)
class Config:
    primary_key: str
    mandatory_columns: list[str]
    date_column: str
    date_format: str
    email_column: str


@dataclass(frozen=True)
class SanitizeResult:
    cleaned_rows: list[Row]
    rejected_rows: list[tuple[Row, str]]
    total_input: int
    duplicate_count: int
    invalid_count: int
