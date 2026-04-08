# src/tests/test_duplicate.py

import unittest

from sanitizer.duplicate import DuplicateChecker
from sanitizer.models import Row


class TestDuplicate(unittest.TestCase):
    def test_first_occurrence_is_valid(self) -> None:
        checker = DuplicateChecker(key_column="email")
        row = Row(data={"email": "test@test.com"}, line_number=1)
        result = checker.check(row)
        self.assertTrue(result.is_valid)

    def test_second_occurrence_is_invalid(self) -> None:
        checker = DuplicateChecker(key_column="email")
        row1 = Row(data={"email": "test@test.com"}, line_number=1)
        result1 = checker.check(row1)
        row2 = Row(data={"email": "test@test.com"}, line_number=2)
        result2 = checker.check(row2)
        self.assertTrue(result1.is_valid)
        self.assertFalse(result2.is_valid)

    def test_different_values_are_valid(self) -> None:
        checker = DuplicateChecker(key_column="email")
        row1 = Row(data={"email": "test@test.com"}, line_number=1)
        result1 = checker.check(row1)
        row2 = Row(data={"email": "example@example.com"}, line_number=2)
        result2 = checker.check(row2)
        self.assertTrue(result1.is_valid)
        self.assertTrue(result2.is_valid)

    def test_reset_clears_seen_values(self) -> None:
        checker = DuplicateChecker(key_column="email")
        row1 = Row(data={"email": "test@test.com"}, line_number=1)
        result1 = checker.check(row1)
        checker.reset()
        row2 = Row(data={"email": "test@test.com"}, line_number=2)
        result2 = checker.check(row2)
        self.assertTrue(result1.is_valid)
        self.assertTrue(result2.is_valid)
