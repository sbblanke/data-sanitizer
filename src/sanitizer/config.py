import json
import sys

from sanitizer.models import Config


def load_config(path: str) -> Config:
    try:
        with open(path, "r") as f:
            data = json.load(f)
            required_keys = [
                "primary_key",
                "mandatory_columns",
                "date_column",
                "date_format",
                "email_column",
            ]
            missing = []
            for key in required_keys:
                if key not in data:
                    missing.append(key)
            if missing:
                sys.exit(
                    f"The following columns are missing from rules.json: {missing}"
                )
            return Config(
                data["primary_key"],
                data["mandatory_columns"],
                data["date_column"],
                data["date_format"],
                data["email_column"],
            )
    except FileNotFoundError:
        sys.exit(f"Error: rules file not found: {path}")
    except json.JSONDecodeError as e:
        sys.exit(f"Error: invalid JSON in rules file: {e}")
