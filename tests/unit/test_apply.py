import pytest

from main import apply_aggregation, apply_filter


@pytest.mark.parametrize(
    "column, operator, value, expected_count",
    [
        ("price", ">", "500", 5),
        ("price", ">=", "999", 3),
        ("price", "<", "200", 2),
        ("price", "<=", "299", 3),
        ("price", "=", "999", 2),
        ("brand", "=", "apple", 4),
        ("brand", "=", "XIAOMI", 3),
    ],
)
def test_apply_filter(test_dict_data, column, operator, value, expected_count):
    result = apply_filter(test_dict_data, column, operator, value)
    assert isinstance(result, list)
    assert len(result) == expected_count


def test_apply_filter_unsupported_operator(test_dict_data):
    with pytest.raises(ValueError, match="Unsupported operator"):
        apply_filter(test_dict_data, "price", "!=", "500")


#  ====================


@pytest.mark.parametrize(
    "column, operation, expected_value",
    [
        ("price", "avg", pytest.approx(602.0, abs=1e-1)),
        ("price", "min", 149.0),
        ("price", "max", 1199.0),
        ("rating", "avg", pytest.approx(4.49, abs=1e-2)),
    ],
)
def test_apply_aggregation_success(test_dict_data, column, operation, expected_value):
    result = apply_aggregation(test_dict_data, column, operation)
    assert isinstance(result, dict)
    assert result["operation"] == operation
    assert result["column"] == column
    assert result["value"] == expected_value


def test_apply_aggregation_invalid_column(test_dict_data):
    with pytest.raises(ValueError, match="Cannot aggregate non-numeric column"):
        apply_aggregation(test_dict_data, "name", "avg")


def test_apply_aggregation_invalid_operation(test_dict_data):
    with pytest.raises(ValueError, match="Unsuppoeted operation"):
        apply_aggregation(test_dict_data, "price", "sum")


def test_apply_aggregation_empty_data():
    result = apply_aggregation([], "price", "avg")
    assert result == {"operation": "avg", "column": "price", "value": "N/A"}
