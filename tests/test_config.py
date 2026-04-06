import unittest
import tempfile
import os
import json

from sanitizer.models import Config
from sanitizer.config import load_config


class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        for f in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, f))
        os.rmdir(self.temp_dir)

    def write_temp_rules_file(self, data: dict) -> str:
        path = os.path.join(self.temp_dir, "rules.json")
        with open(path, "w") as f:
            json.dump(data, f)
        return path

    def test_valid_config(self) -> None:
        path = self.write_temp_rules_file(
            {
                "primary_key": "email",
                "mandatory_columns": ["first_name", "last_name", "email"],
                "date_column": "date_of_birth",
                "date_format": "%Y-%m-%d",
                "email_column": "email",
            }
        )
        result = load_config(path)
        self.assertEqual(result.primary_key, "email")
        self.assertEqual(result.date_format, "%Y-%m-%d")

    # TODO - finish these tests
    def test_missing_file(self) -> None:
        raise NotImplementedError

    def test_invalid_json(self) -> None:
        raise NotImplementedError

    def test_missing_key(self) -> None:
        raise NotImplementedError

    def test_extra_keys_allowed(self) -> None:
        raise NotImplementedError
