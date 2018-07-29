from numpy import array as np_array, zeros as np_zeros, linspace, around
import pytest

from pydcf.correlators import gdcf


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
def test_time_parameters():
    dt = 2
    lgl = -7
    lgh = 7
    n = around((lgh - lgl) / float(dt))
    t = linspace(lgl + (dt/2.0), lgh - (dt/2.0), n)
    return (t, dt)

def test_gdcf(test_ts):

    expected_dcf = np_array([
        0.05272416,
        -0.53167306,
        0.06199813,
        0.81247255,
        0.06199813,
        -0.53167306,
        0.05272416,
    ])

    expected_dcferr = np_array([
        0.27102338,
        0.25074062,
        0.24015341,
        0.30209551,
        0.24015341,
        0.25074062,
        0.27102338,
    ])
    
    output_dcf, output_dcferr = gdcf(test_ts, test_ts, *test_time_parameters())

    assert all([around(a, decimals=3) == around(b, decimals=3) for a, b in zip(output_dcf, expected_dcf)])
    assert all([around(a, decimals=3) == around(b, decimals=3) for a, b in zip(output_dcferr, expected_dcferr)])
