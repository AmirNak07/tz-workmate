import csv

import pytest

from main import read_csv


def test_read_csv_success(tmp_path):
    file_path = tmp_path / "test_data.csv"
    data = [
        {"name": "iphone", "price": "999"},
        {"name": "galaxy", "price": "899"},
    ]

    with file_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price"])
        writer.writeheader()
        writer.writerows(data)

    result = read_csv(str(file_path))

    assert isinstance(result, list)
    assert result == data


def test_read_csv_empty_file(tmp_path):
    file_path = tmp_path / "empty.csv"
    with file_path.open("w", encoding="utf-8", newline="") as f:
        f.write("name,price\n")

    result = read_csv(str(file_path))
    assert result == []


def test_read_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_csv("non_existent_file.csv")
