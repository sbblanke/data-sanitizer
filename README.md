# data-sanitizer

A CLI tool that cleans CSV exports by removing duplicates and validating data based on email addresses and dates.

---

## Features

- Deduplicates rows based on a key column
- Validates dates are in the proper format
- Validates emails are in the proper format
- Separates clean and rejected rows into separate CSVs
- Creates an audit log for duplicates, rejected rows, and summary details per run
- Dry-run functionality to check what will happen before adjusting anything

---

## Requirements

- Python version: 3.13+
- Clone into repo to start using:
    `git clone https://github.com/sbblanke/data-sanitizer.git`
- Use `uv sync` to install dependencies

---

## Configuration

This project uses a `rules.json` file to set the configuration for your specific CSV. This is where you can identify the values to use for your specific use case. as the basis for deduplication (primary_key), indicate columns that are mandatory to support repetitive workflows where additional data shouldn't crash the program, identify the date and email columns, and indicate which date format you want to use.

```json
{
    "primary_key": "",
    "mandatory_columns": [],
    "date_column": "",
    "date_format": "",
    "email_column": ""
}
```

Explain each field here:

| Field | Description |
|-------|-------------|
| `primary_key` | The column used to identify duplicate rows. e.g. "id" |
| `mandatory_columns` | List of columns that must be present in the CSV. e.g. ["first_name", "email"] |
| `date_column` | The column containing dates to validate. e.g. "date_of_birth" |
| `date_format` | The expected date format using Python strftime codes. e.g. "%Y-%m-%d" for 2026-12-13 |
| `email_column` | The column containing email addresses to validate. e.g. "email" |

---

## Usage

```bash
# Basic run (deduplication only)
uv run python main.py sample.csv

# Enable date validation
uv run python main.py sample.csv --date

# Enable email validation
uv run python main.py sample.csv --email

# Enable all validations
uv run python main.py sample.csv --all

# Dry run (preview without writing files)
uv run python main.py sample.csv --dry-run

# Custom rules file
uv run python main.py sample.csv --rules <file>
```

---

## Output

Describe the three output files and what each contains.

| File | Description |
|------|-------------|
| `_cleaned.csv` | Rows that passed all checks |
| `_rejected.csv` | Rows that failed, with a rejection_reason column added |
| `_audit_log.log` | Timestamped log of every rejection and a run summary |

---

## Running Tests

```bash
uv run python -m unittest discover tests
```
