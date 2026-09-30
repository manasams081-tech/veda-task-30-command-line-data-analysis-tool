#!/usr/bin/env python3
"""
VEDA Technology Task 30
Build a Command-Line Data Analysis Tool

Examples:
  python cli_tool.py --file sample_data/sales.csv --summary
  python cli_tool.py --file sample_data/sales.csv --filter region South
  python cli_tool.py --file sample_data/sales.csv --group region --metric sales
  python cli_tool.py --file sample_data/sales.csv --stats sales
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path

from analysis import (
    DataAnalysisError,
    filter_data,
    group_data,
    load_csv,
    preview,
    statistics,
    summary,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="veda-analyzer",
        description=(
            "VEDA Task 30 - Analyze any CSV using reusable Pandas operations."
        ),
        epilog=(
            "Commands are selected with flags. The dataset filename is never "
            "hardcoded, so the same tool works with different CSV files."
        ),
    )
    parser.add_argument(
        "--file", required=True, help="Path to the CSV dataset."
    )

    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--summary", action="store_true", help="Show dataset summary.")
    action.add_argument(
        "--preview", type=int, nargs="?", const=10, metavar="N",
        help="Show the first N rows (default: 10)."
    )
    action.add_argument(
        "--filter", nargs=2, metavar=("COLUMN", "VALUE"),
        help="Filter rows using a column and value."
    )
    action.add_argument(
        "--group", metavar="COLUMN",
        help="Group records by a column."
    )
    action.add_argument(
        "--stats", metavar="COLUMN",
        help="Show descriptive statistics for a numeric column."
    )

    parser.add_argument(
        "--metric", metavar="COLUMN",
        help="Numeric metric for --group (count/sum/mean/min/max)."
    )
    parser.add_argument(
        "--limit", type=int, default=20,
        help="Maximum rows displayed for tabular results (default: 20)."
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Return machine-readable JSON where supported."
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        df = load_csv(args.file)

        if args.summary:
            result = summary(df)
            print(json.dumps(result, indent=2) if args.json else format_summary(result))

        elif args.preview is not None:
            result = preview(df, args.preview)
            print(json.dumps(result, indent=2, default=str) if args.json
                  else format_records(result))

        elif args.filter:
            column, value = args.filter
            result = filter_data(df, column, value).head(args.limit)
            print(json.dumps(result.to_dict("records"), indent=2, default=str)
                  if args.json else result.to_string(index=False))

        elif args.group:
            result = group_data(df, args.group, args.metric).head(args.limit)
            print(json.dumps(result.to_dict("records"), indent=2, default=str)
                  if args.json else result.to_string(index=False))

        elif args.stats:
            result = statistics(df, args.stats)
            print(json.dumps(result, indent=2) if args.json else format_stats(result))

        return 0

    except DataAnalysisError as exc:
        print(f"ERROR: {exc}")
        return 2


def format_summary(result: dict) -> str:
    lines = [
        "VEDA DATASET SUMMARY",
        "====================",
        f"Rows              : {result['rows']}",
        f"Columns           : {result['columns']}",
        f"Missing values    : {result['missing_values']}",
        f"Numeric columns   : {', '.join(result['numeric_columns']) or 'None'}",
        f"Column names      : {', '.join(result['column_names'])}",
    ]
    return "\n".join(lines)


def format_stats(result: dict) -> str:
    return "\n".join([
        "DESCRIPTIVE STATISTICS",
        "======================",
        f"Count   : {result['count']}",
        f"Mean    : {result['mean']:.2f}",
        f"Median  : {result['median']:.2f}",
        f"Min     : {result['min']:.2f}",
        f"Max     : {result['max']:.2f}",
        f"Std Dev : {result['std']:.2f}",
        f"Sum     : {result['sum']:.2f}",
    ])


def format_records(records: list[dict]) -> str:
    if not records:
        return "No records found."
    headers = list(records[0].keys())
    widths = {h: max(len(str(h)), *(len(str(r.get(h, ""))) for r in records)) for h in headers}
    line = " | ".join(str(h).ljust(widths[h]) for h in headers)
    sep = "-+-".join("-" * widths[h] for h in headers)
    body = [" | ".join(str(r.get(h, "")).ljust(widths[h]) for h in headers) for r in records]
    return "\n".join([line, sep, *body])


if __name__ == "__main__":
    raise SystemExit(main())
