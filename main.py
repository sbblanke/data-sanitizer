from sanitizer.cli import parse_args
from sanitizer.config import load_config
from sanitizer.reader import read_csv
from sanitizer.pipeline import Pipeline
from sanitizer.validators.date import DateValidator
from sanitizer.validators.email import EmailValidator
from sanitizer.duplicate import DuplicateChecker
from sanitizer.models import SanitizeResult
from sanitizer.writer import write_clean_csv, write_rejected_csv


def print_summary(result: SanitizeResult, input_path: str, dry_run: bool) -> None:
    if dry_run:
        label = "DRY RUN "
    else:
        label = ""

    print(f"\n--- Summary {label}---")
    print(f"Input file:    {input_path}")
    print(f"Total rows:    {result.total_input}")
    print(f"Cleaned:       {len(result.cleaned_rows)}")
    print(f"Rejected:      {len(result.rejected_rows)}")
    print(f"  Duplicates:  {result.duplicate_count}")
    print(f"  Invalid:     {result.invalid_count}")


def main():
    args = parse_args()
    config = load_config(args.rules)
    rows = read_csv(args.input_file, config)

    validators = []
    if args.date or args.all:
        validators.append(
            DateValidator(column=config.date_column, date_format=config.date_format)
        )
    if args.email or args.all:
        validators.append(EmailValidator(column=config.email_column))
    checker = DuplicateChecker(key_column=config.primary_key)
    pipeline = Pipeline(duplicate_checker=checker, validators=validators)
    result = pipeline.run(rows)
    if not args.dry_run:
        clean_output_path = args.input_file.replace(".csv", "_cleaned.csv")
        rejected_output_path = args.input_file.replace(".csv", "_rejected.csv")
        write_clean_csv(clean_output_path, result.cleaned_rows)
        write_rejected_csv(rejected_output_path, result.rejected_rows)

    print_summary(result, args.input_file, args.dry_run)


if __name__ == "__main__":
    main()
