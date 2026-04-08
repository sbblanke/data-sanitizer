import unittest
from sanitizer.validators.email import EmailValidator
from sanitizer.models import Row


class TestEmail(unittest.TestCase):
    def test_valid_email(self) -> None:
        validator = EmailValidator(column="email")
        row = Row(data={"email": "test@test.com"}, line_number=1)
        result = validator.validate(row)
        self.assertTrue(result.is_valid)

    def test_missing_at_sign(self) -> None:
        validator = EmailValidator(column="email")
        row = Row(data={"email": "testtest.com"}, line_number=1)
        result = validator.validate(row)
        self.assertFalse(result.is_valid)

    def test_empty_value(self) -> None:
        validator = EmailValidator(column="email")
        row = Row(data={"email": ""}, line_number=1)
        result = validator.validate(row)
        self.assertFalse(result.is_valid)

    def test_rejection_reason(self) -> None:
        validator = EmailValidator(column="email")
        row = Row(data={"email": "invalidemail"}, line_number=1)
        result = validator.validate(row)
        self.assertEqual(result.rejection_reason, "invalid:email")
