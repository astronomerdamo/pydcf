from __future__ import print_function

import pytest
import numpy as np

from pydcf.dcf import set_unitytime 

#@pytest.fixture()
#def test_timeseries():
#    return []


def test_dummy():
    assert set_unitytime()
