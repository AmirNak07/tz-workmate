import argparse
import csv

from tabulate import tabulate


def read_csv(file_path: str):
    with open(file_path, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def parse_where_param(where: str):
    operators = [">=", "<=", ">", "<", "="]
    for op in operators:
        if op in where:
            parts = where.split(op)
            if len(parts) == 2:
                return parts[0], op, parts[1]
    raise ValueError(f"Invalid where parameter: {where}")


def parse_aggregate_param(aggregate: str):
    parts = aggregate.split("=")
    if len(parts) != 2:
        raise ValueError(f"Invalid aggregate parameter: {aggregate}")
    return parts[0], parts[1]


def apply_filter(data, column, operator, value):
    operators = {
        ">": lambda x, y: x > y,
        ">=": lambda x, y: x >= y,
        "<": lambda x, y: x < y,
        "<=": lambda x, y: x <= y,
        "=": lambda x, y: x == y,
    }

    op_func = operators.get(operator)
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


def apply_aggregation(data, column, operation):
    try:
        values = [float(row[column]) for row in data]
    except ValueError:
        raise ValueError(f"Cannot aggregate non-numeric column: {column}") from None

    if not values:
        return {"operation": operation, "column": column, "value": "N/A"}

    operations = {"avg": lambda x: sum(x) / len(x), "min": min, "max": max}

    op_func = operations.get(operation)
    if op_func is None:
        raise ValueError(f"Unsuppoeted operation: {operation}")

    result = op_func(values)
    return {"operation": operation, "column": column, "value": result}


def main() -> None:
    parser = argparse.ArgumentParser(description="Process CSV file.")
    parser.add_argument("--file", help="Path to CSV file", required=True, dest="<FILE_PATH>")
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
        print(tabulate([[result["value"]]], headers=[result["operation"]], tablefmt="grid"))
    else:
        print(tabulate(data, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    main()
