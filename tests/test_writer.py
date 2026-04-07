# test_writer.py

import unittest
import tempfile
import os
import csv
import logging

from sanitizer.models import Row
from sanitizer.writer import write_clean_csv, write_rejected_csv, setup_audit_log


class TestWriter(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        for f in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, f))
        os.rmdir(self.temp_dir)

    def make_row(self, email: str, line_number: int) -> Row:
        return Row(
            data={"email": email, "first_name": "John", "last_name": "Smith"},
            line_number=line_number,
        )

    def test_write_clean_csv(self) -> None:
        rows = [
            self.make_row("test@test.com", 1),
            self.make_row("example@example.com", 2),
        ]
        path = os.path.join(self.temp_dir, "cleaned.csv")
        write_clean_csv(path, rows)
        with open(path, newline="") as f:
            written = list(csv.DictReader(f))

        self.assertEqual(len(written), 2)
        self.assertEqual(written[0]["email"], "test@test.com")
        self.assertEqual(written[1]["email"], "example@example.com")

    def test_write_clean_csv_empty(self) -> None:
        rows: list = []  # create empty list
        path = os.path.join(self.temp_dir, "cleaned.csv")
        write_clean_csv(path, rows)
        self.assertFalse(os.path.exists(path))

    def test_write_rejected_csv(self) -> None:
        rejected = [
            (self.make_row("test@test.com", 1), "duplicate: email"),
            (self.make_row("example@example.com", 2), "unknown_reason"),
        ]
        path = os.path.join(self.temp_dir, "rejected.csv")
        write_rejected_csv(path, rejected)
        with open(path, newline="") as f:
            written = list(csv.DictReader(f))

        self.assertEqual(len(written), 2)
        self.assertEqual(written[0]["rejection_reason"], "duplicate: email")
        self.assertEqual(written[1]["rejection_reason"], "unknown_reason")

    def test_setup_audit_log(self) -> None:
        path = os.path.join(self.temp_dir, "audit.log")
        setup_audit_log(path)
        logging.info("test message")

        with open(path) as f:
            contents = f.read()

        self.assertIn("test message", contents)
