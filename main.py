import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Process CSV file.")
    parser.add_argument("file", help="Path to CSV file")
    parser.add_argument(
        "--where", help='Filter condition (e.g., "price>500")', type=str
    )
    parser.add_argument(
        "--aggregate", help='Aggregate orepation (e.g., "avg=price")', type=str
    )

    args = parser.parse_args()

    print(args)


if __name__ == "__main__":
    main()
