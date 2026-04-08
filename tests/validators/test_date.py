# test_date.py

import unittest
from sanitizer.validators.date import DateValidator
from sanitizer.models import Row


class TestDate(unittest.TestCase):
    def test_valid_date(self) -> None:
        validator = DateValidator(column="dob", date_format="%Y-%m-%d")
        row = Row(data={"dob": "1999-01-01"}, line_number=1)
        result = validator.validate(row)
        self.assertTrue(result.is_valid)

    def test_invalid_date(self) -> None:
        validator = DateValidator(column="dob", date_format="%Y-%m-%d")
        row = Row(data={"dob": "not a date"}, line_number=1)
        result = validator.validate(row)
        self.assertFalse(result.is_valid)

    def test_empty_value(self) -> None:
        validator = DateValidator(column="dob", date_format="%Y-%m-%d")
        row = Row(data={"dob": ""}, line_number=1)
        result = validator.validate(row)
        self.assertFalse(result.is_valid)

    def test_rejection_reason(self) -> None:
        validator = DateValidator(column="dob", date_format="%Y-%m-%d")
        row = Row(data={"dob": ""}, line_number=1)
        result = validator.validate(row)
        self.assertEqual(result.rejection_reason, "invalid:dob")
