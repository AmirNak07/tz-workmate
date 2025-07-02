from contextlib import nullcontext as does_not_raise

import pytest

from main import parse_aggregate_param, parse_where_param


@pytest.mark.parametrize(
    "input_str,expected_col,expected_op,expected_val, expected_err",
    [
        ("price>500", "price", ">", "500", does_not_raise()),
        ("price>=3500", "price", ">=", "3500", does_not_raise()),
        ("price<0", "price", "<", "0", does_not_raise()),
        ("price<=1000", "price", "<=", "1000", does_not_raise()),
        ("price=200", "price", "=", "200", does_not_raise()),
        ("price", "price", "", "", pytest.raises(ValueError)),
        ("price100", "price", "", "100", pytest.raises(ValueError)),
        ("price<", "price", "<", "", pytest.raises(ValueError)),
        (">=100", "", ">=", "100", pytest.raises(ValueError)),
        ("price>=price", "price", ">=", "price", does_not_raise()),
    ],
)
def test_parse_where_param(
    input_str, expected_col, expected_op, expected_val, expected_err
):
    with expected_err:
        col, op, val = parse_where_param(input_str)
        assert col == expected_col
        assert op == expected_op
        assert val == expected_val


@pytest.mark.parametrize(
    "input_str,expected_col,expected_op, expected_err",
    [
        ("price=min", "price", "min", does_not_raise()),
        ("price=max", "price", "max", does_not_raise()),
        ("price=avg", "price", "avg", does_not_raise()),
        ("price=test", "price", "test", does_not_raise()),
        ("price>avg", "price", "avg", pytest.raises(ValueError)),
        ("price", "price", "", pytest.raises(ValueError)),
        ("=", "", "", pytest.raises(ValueError)),
    ],
)
def test_parse_aggregate_param(input_str, expected_col, expected_op, expected_err):
    with expected_err:
        col, op = parse_aggregate_param(input_str)
        assert col == expected_col
        assert op == expected_op
