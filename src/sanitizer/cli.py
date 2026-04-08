# src/sanitizer/cli.py

import argparse


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean CSV files by removing duplicates and validating emails and dates."
    )

    parser.add_argument("input_file", help="Path to the input CSV file")

    parser.add_argument("--rules", default="rules.json", help="Path to rules.json")
    parser.add_argument("--date", action="store_true", help="Enable date validation")
    parser.add_argument("--email", action="store_true", help="Enable email validation")
    parser.add_argument(
        "--dry-run", action="store_true", help="Dry run without creating docs"
    )
    parser.add_argument(
        "--all", action="store_true", help="Runs the email and date validation"
    )

    return parser.parse_args(argv)
