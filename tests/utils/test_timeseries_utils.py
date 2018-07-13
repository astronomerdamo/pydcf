from __future__ import print_function

from numpy import array as np_array, zeros as np_zeros
import pytest

from pydcf.utils import set_unitytime, validate_timeseries


@pytest.fixture
def test_ts1():
    return np_array([
        [11., 1., 0.1],
        [13., 3., 0.1],
        [14., 4., 0.1],
    ])


@pytest.fixture
def test_ts2():
    return np_array([
        [21., 1., 0.1],
        [22., 2., 0.1],
        [24., 4., 0.1],
    ])


@pytest.fixture
def array_equality_test_helper(expected_ts, output_ts):
    return all(a == b for row_a, row_b in zip(expected_ts, output_ts) for a, b in zip(row_a, row_b))


def test_set_unitytime(test_ts1, test_ts2):
    expected_ts1 = np_array([
        [0., 1., 0.1],
        [2., 3., 0.1],
        [3., 4., 0.1],
    ])

    expected_ts2 = np_array([
        [10., 1., 0.1],
        [11., 2., 0.1],
        [13., 4., 0.1],
    ])

    output_ts1, output_ts2 = set_unitytime(test_ts1, test_ts2)

    assert array_equality_test_helper(expected_ts1, output_ts1)
    assert array_equality_test_helper(expected_ts2, output_ts2)


def test_validate_timeseries(test_ts1):
    test_ts_2_col = test_ts1[:, :2]
    test_ts_4_col = np_zeros((test_ts1.shape[0], 4))

    expected_test_ts_2_col = np_zeros((test_ts1.shape[0], 3))
    expected_test_ts_2_col[:, :2] = test_ts_2_col

    assert array_equality_test_helper(validate_timeseries(test_ts1), test_ts1)
    assert array_equality_test_helper(validate_timeseries(test_ts_2_col), expected_test_ts_2_col)
