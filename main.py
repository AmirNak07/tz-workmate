import argparse
import csv
import re
from collections.abc import Callable
from typing import Any

from tabulate import tabulate


def read_csv(file_path: str) -> list[dict[str, str]]:
    """Read CSV file and return list of dictionaries."""
    with open(file_path, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def parse_where_param(where: str) -> tuple[str, str, str]:
    """Parse where parameter into column, operator, value."""
    pattern = r"^([^<>=!]+)(>=|<=|=|<|>)(.+)$"
    m = re.match(pattern, where)
    if not m:
        raise ValueError(f"Invalid where parameter: {where}")
    col, op, val = m.groups()

    if not col or not val:
        raise ValueError(f"Invalid where parameter: {where}")
    return col, op, val


def parse_aggregate_param(aggregate: str) -> tuple[str, str]:
    """Parse aggregate parameter into operation and column."""
    parts = aggregate.split("=")
    if len(parts) != 2 or parts[0] == "" or parts[1] == "":
        raise ValueError(f"Invalid aggregate parameter: {aggregate}")
    return parts[0], parts[1]


def apply_filter(
    data: list[dict[str, str]], column: str, operator: str, value: str
) -> list[dict[str, str]]:
    """Filter data based on column, operator and value."""
    operators = {
        ">": lambda x, y: x > y,
        ">=": lambda x, y: x >= y,
        "<": lambda x, y: x < y,
        "<=": lambda x, y: x <= y,
        "=": lambda x, y: x == y,
    }

    op_func: Callable[[Any, Any], bool] | None = operators.get(operator)
    if op_func is None:
        raise ValueError("Unsupported operator: {operator}")

    filtered = []
    for row in data:
        try:
            row_val = float(row[column]) if "." in row[column] else int(row[column])
            cmp_val = float(value) if "." in value else int(value)
            if op_func(row_val, cmp_val):
                filtered.append(row)
        except ValueError:
            if op_func(row[column].lower(), value.lower()):
                filtered.append(row)

    return filtered


def apply_aggregation(
    data: list[dict[str, str]], column: str, operation: str
) -> dict[str, float | str]:
    """Apply aggregation operation on numeric column."""
    try:
        values = [float(row[column]) for row in data]
    except ValueError:
        raise ValueError(f"Cannot aggregate non-numeric column: {column}") from None

    if not values:
        return {"operation": operation, "column": column, "value": "N/A"}

    operations: dict[str, Callable[[list[float]], float]] = {
        "avg": lambda x: sum(x) / len(x),
        "min": min,
        "max": max,
    }

    op_func: Callable[[list[float]], float] | None = operations.get(operation)
    if op_func is None:
        raise ValueError(f"Unsuppoeted operation: {operation}")

    result = op_func(values)
    return {"operation": operation, "column": column, "value": result}


def main() -> None:
    parser = argparse.ArgumentParser(description="Process CSV file.")
    parser.add_argument(
        "--file", help="Path to CSV file", required=True, dest="<FILE_PATH>"
    )
    parser.add_argument(
        "--where", help='Filter condition (e.g., "price>500")', type=str, dest=""
    )
    parser.add_argument(
        "--aggregate", help='Aggregate orepation (e.g., "avg=price")', type=str, dest=""
    )

    args = parser.parse_args()

    data = read_csv(args.file)

    if args.where:
        column, operator, value = parse_where_param(args.where)
        data = apply_filter(data, column, operator, value)

    if args.aggregate:
        column, operation = parse_aggregate_param(args.aggregate)
        result = apply_aggregation(data, column, operation)
        print(
            tabulate(
                [[result["value"]]], headers=[str(result["operation"])], tablefmt="grid"
            )
        )
    else:
        print(tabulate(data, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    main()
