import csv
import os
import tempfile
import unittest
from sanitizer.reader import read_csv
from sanitizer.models import Config, Row


class TestReader(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        for f in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, f))
        os.rmdir(self.temp_dir)

    def write_temp_csv(self) -> str:
        path = os.path.join(self.temp_dir, "test.csv")
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["email", "first_name", "last_name", "date_of_birth"]
            )
            writer.writeheader()
            writer.writerows(
                [
                    {
                        "email": "test@test.com",
                        "first_name": "John",
                        "last_name": "Smith",
                        "date_of_birth": "1990-01-01",
                    },
                    {
                        "email": "example@example.com",
                        "first_name": "Bob",
                        "last_name": "Jones",
                        "date_of_birth": "1988-06-15",
                    },
                ]
            )
        return path

    def sample_config(self) -> Config:
        return Config(
            primary_key="email",
            mandatory_columns=["first_name", "last_name", "email"],
            date_column="date_of_birth",
            date_format="%Y-%m-%d",
            email_column="email",
        )

    def test_returns_correct_row_count(self) -> None:
        path = self.write_temp_csv()
        config = self.sample_config()
        result = read_csv(path, config)
        self.assertEqual(len(result), 2)

    def test_row_data_matches_csv(self) -> None:
        path = self.write_temp_csv()
        config = self.sample_config()
        result = read_csv(path, config)
        self.assertEqual(
            result[0],
            Row(
                data={
                    "email": "test@test.com",
                    "first_name": "John",
                    "last_name": "Smith",
                    "date_of_birth": "1990-01-01",
                },
                line_number=1,
            ),
        )

    def test_line_numbers_are_correct(self) -> None:
        path = self.write_temp_csv()
        config = self.sample_config()
        result = read_csv(path, config)
        self.assertEqual(result[0].line_number, 1)
        self.assertEqual(result[1].line_number, 2)

    def test_missing_file(self) -> None:
        path = ""
        config = self.sample_config()
        with self.assertRaises(SystemExit):
            read_csv(path, config)

    def test_empty_csv(self) -> None:
        path = os.path.join(self.temp_dir, "test.csv")
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["email", "first_name", "last_name", "date_of_birth"]
            )
            writer.writeheader()  # header only
        config = self.sample_config()
        with self.assertRaises(SystemExit):
            read_csv(path, config)
