import unittest

from sanitizer.models import Row, ValidationResult, Config, SanitizeResult
from dataclasses import FrozenInstanceError


class TestModels(unittest.TestCase):
    def test_row_creation(self) -> None:
        row = Row(data={"1": "a", "2": "b", "3": "c"}, line_number=10)
        self.assertEqual(row.data, {"1": "a", "2": "b", "3": "c"})
        self.assertEqual(row.line_number, 10)

    def test_row_is_immutable(self) -> None:
        row = Row(data={"1": "a", "2": "b", "3": "c"}, line_number=10)
        with self.assertRaises(FrozenInstanceError):
            setattr(row, "data", {})

    def test_validation_result_defaults(self) -> None:
        result = ValidationResult(is_valid=True)
        self.assertEqual(result.rejection_reason, "")

    def test_config_creation(self) -> None:
        config = Config(
            primary_key="Id",
            mandatory_columns=["first_name", "last_name"],
            date_column="example_date",
            date_format="%Y-%m-%d",
            email_column="email",
        )
        self.assertEqual(config.date_column, "example_date")
        self.assertEqual(config.primary_key, "Id")

    def test_sanitize_result_counts(self) -> None:
        row = Row(data={"email": "test@test.com"}, line_number=1)
        result = SanitizeResult(
            cleaned_rows=[row],
            rejected_rows=[(row, "duplicate:email")],
            total_input=2,
            duplicate_count=1,
            invalid_count=0,
        )
        self.assertEqual(result.total_input, 2)
        self.assertEqual(result.duplicate_count, 1)
        self.assertEqual(result.invalid_count, 0)
