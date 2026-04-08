import unittest

from sanitizer.pipeline import Pipeline
from sanitizer.duplicate import DuplicateChecker
from sanitizer.models import Row
from sanitizer.validators.email import EmailValidator
from sanitizer.validators.date import DateValidator


class TestPipeline(unittest.TestCase):
    def setUp(self) -> None:
        self.email_validator = EmailValidator(column="email")
        self.date_validator = DateValidator(column="dob", date_format="%Y-%m-%d")

    def test_no_validators_all_cleaned(self) -> None:
        checker = DuplicateChecker(key_column="email")
        pipeline = Pipeline(duplicate_checker=checker, validators=[])
        rows = [Row(data={"email": "test@test.com"}, line_number=1)]
        result = pipeline.run(rows)
        self.assertEqual(len(result.cleaned_rows), 1)
        self.assertEqual(len(result.rejected_rows), 0)

    def test_duplicate_goes_to_rejected(self) -> None:
        checker = DuplicateChecker(key_column="email")
        pipeline = Pipeline(duplicate_checker=checker, validators=[])
        rows = [
            Row(data={"email": "test@test.com"}, line_number=1),
            Row(data={"email": "test@test.com"}, line_number=2),
        ]
        result = pipeline.run(rows)
        self.assertEqual(len(result.cleaned_rows), 1)
        self.assertEqual(len(result.rejected_rows), 1)
        self.assertEqual(result.rejected_rows[0][1], "duplicate:email")

    def test_invalid_row_goes_to_rejected(self) -> None:
        checker = DuplicateChecker(key_column="email")
        pipeline = Pipeline(
            duplicate_checker=checker, validators=[self.email_validator]
        )
        rows = [Row(data={"email": "invalid email"}, line_number=1)]
        result = pipeline.run(rows)
        self.assertEqual(len(result.cleaned_rows), 0)
        self.assertEqual(len(result.rejected_rows), 1)
        self.assertEqual(result.rejected_rows[0][1], "invalid:email")

    def test_valid_row_goes_to_cleaned(self) -> None:
        checker = DuplicateChecker(key_column="dob")
        pipeline = Pipeline(duplicate_checker=checker, validators=[self.date_validator])
        rows = [Row(data={"dob": "2000-01-01"}, line_number=1)]
        result = pipeline.run(rows)
        self.assertEqual(len(result.cleaned_rows), 1)
        self.assertEqual(len(result.rejected_rows), 0)

    def test_duplicate_count_is_correct(self) -> None:
        checker = DuplicateChecker(key_column="email")
        pipeline = Pipeline(duplicate_checker=checker, validators=[])
        rows = [
            Row(data={"email": "test@test.com"}, line_number=1),
            Row(data={"email": "test@test.com"}, line_number=2),
        ]
        result = pipeline.run(rows)
        self.assertEqual(result.duplicate_count, 1)

    def test_validator_short_circuits(self) -> None:
        checker = DuplicateChecker(key_column="email")
        pipeline = Pipeline(
            duplicate_checker=checker,
            validators=[self.date_validator, self.email_validator],
        )
        rows = [
            Row(data={"dob": "invalid date", "email": "invalid email"}, line_number=1)
        ]
        result = pipeline.run(rows)
        self.assertEqual(len(result.cleaned_rows), 0)
        self.assertEqual(len(result.rejected_rows), 1)  # confirms loop breaks
