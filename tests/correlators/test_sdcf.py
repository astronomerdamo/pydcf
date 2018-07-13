from numpy import array as np_array, zeros as np_zeros, linspace, around
import pytest

from pydcf.correlators import sdcf


@pytest.fixture
def test_ts():
    return np_array([
        [0.0, 1., 0.1],
        [1.1, 1., 0.1],
        [1.9, 3., 0.1],
        [3.2, 7., 0.1],
        [3.9, 9., 0.1],
        [6.1, 2., 0.1],
        [7.7, 1., 0.1],
        [8.5, 2., 0.1],
        [9.4, 3., 0.1],
        [9.8, 1., 0.1],
    ])


@pytest.fixture
def test_ts2():
    return np_array([
        [21., 1., 0.1],
        [22., 2., 0.1],
        [24., 4., 0.1],
    ])


def test_sdcf(test_ts):
    # TODO: Build tests for sdcf
    test_dt = 2
    test_lgl = -7
    test_lgh = 7
    n = around((test_lgh - test_lgl) / float(test_dt))
    test_t = linspace(test_lgl+(test_dt/2.0), test_lgh-(test_dt/2.0), n)
    output = sdcf(test_ts, test_ts, test_t, test_dt)
    import pdb; pdb.set_trace()
    assert True
