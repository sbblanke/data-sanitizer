from unittest.mock import patch
import unittest
import csv
import os
import tempfile

from main import main


class TestIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

        # Write a sample CSV
        self.csv_path = os.path.join(self.temp_dir, "sample.csv")
        with open(self.csv_path, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["id", "first_name", "last_name", "email", "date_of_birth"],
            )
            writer.writeheader()
            writer.writerows(
                [
                    {
                        "id": "1",
                        "first_name": "Alice",
                        "last_name": "Smith",
                        "email": "alice@example.com",
                        "date_of_birth": "1990-01-15",
                    },
                    {
                        "id": "2",
                        "first_name": "Bob",
                        "last_name": "Jones",
                        "email": "bob@example.com",
                        "date_of_birth": "1985-06-20",
                    },
                    {
                        "id": "1",
                        "first_name": "Alice",
                        "last_name": "Dup",
                        "email": "alice@example.com",
                        "date_of_birth": "1990-01-15",
                    },
                    {
                        "id": "3",
                        "first_name": "Charlie",
                        "last_name": "Brown",
                        "email": "notanemail",
                        "date_of_birth": "1992-03-10",
                    },
                ]
            )

        self.rules_path = os.path.join(self.temp_dir, "rules.json")
        with open(self.rules_path, "w") as f:
            import json

            json.dump(
                {
                    "primary_key": "id",
                    "mandatory_columns": ["first_name", "last_name", "email"],
                    "date_column": "date_of_birth",
                    "date_format": "%Y-%m-%d",
                    "email_column": "email",
                },
                f,
            )

    def tearDown(self) -> None:
        for f in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, f))
        os.rmdir(self.temp_dir)

    def test_full_run_creates_output_files(self) -> None:
        cleaned_path = self.csv_path.replace(".csv", "_cleaned.csv")
        rejected_path = self.csv_path.replace(".csv", "_rejected.csv")

        with patch(
            "sys.argv",
            ["main.py", self.csv_path, "--rules", self.rules_path, "--email"],
        ):
            main()

        self.assertTrue(os.path.exists(cleaned_path))
        self.assertTrue(os.path.exists(rejected_path))

    def test_dry_run_creates_no_files(self):
        cleaned_path = self.csv_path.replace(".csv", "_cleaned.csv")
        rejected_path = self.csv_path.replace(".csv", "_rejected.csv")

        with patch(
            "sys.argv",
            [
                "main.py",
                self.csv_path,
                "--rules",
                self.rules_path,
                "--email",
                "--dry-run",
            ],
        ):
            main()

        self.assertFalse(os.path.exists(cleaned_path))
        self.assertFalse(os.path.exists(rejected_path))

    def test_correct_rows_in_cleaned_output(self):
        cleaned_path = self.csv_path.replace(".csv", "_cleaned.csv")
        rejected_path = self.csv_path.replace(".csv", "_rejected.csv")

        with patch(
            "sys.argv",
            ["main.py", self.csv_path, "--rules", self.rules_path, "--email"],
        ):
            main()
            with open(cleaned_path, newline="") as f:
                cleaned = list(csv.DictReader(f))

            with open(rejected_path, newline="") as f:
                rejected = list(csv.DictReader(f))

        self.assertEqual(len(cleaned), 2)
        self.assertEqual(len(rejected), 2)
