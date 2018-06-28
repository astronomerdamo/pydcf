from __future__ import print_function

from scipy.optimize import curve_fit as _curve_fit
from numpy import \
     min as _min,\
     zeros as _zeros,\
     mean as _mean,\
     loadtxt as _loadtxt



def set_unitytime(ts1, ts2):

    """
        Subroutine - _set_unitytime
          Simply shifts both time series so that one starts at zero.
    """

    unitytime = min(_min(ts1[:,0]), _min(ts2[:,0]))
    ts1[:,0] = ts1[:,0] - unitytime
    ts2[:,0] = ts2[:,0] - unitytime

    return ts1, ts2

def validate_timeseries(ts):

    """
        Subroutine - _validate_timeseries
          Makes sure user has entered a properly formatted timeseries.
          Checks to see if input time series has a measurement error column - third
          column of input file.
    """

    assert ((ts.shape[1] == 2) or (ts.shape[1] == 3)), "TS SHAPE ERROR"

    if ts.shape[1] == 2:
        ts_fill = _zeros((ts.shape[0], 3))
        ts_fill[:,0:2] = ts[:,0:2]

        return ts_fill

    else:

        return ts

def tsdtrnd(ts, vrbs, plyft):

    """
        Subroutine - tsdtrnd
          Time series detrend using the user chosen polynomial order. Subroutine
          fits a ploynomial to the time series data and subtracts.
    """

    if plyft == 0:

        ts_mean = _mean(ts[:,1])
        ts[:,1] = ts[:,1] - ts_mean
        if vrbs:
            print("Mean subtraction: %.4e" %ts_mean)

    elif plyft == 1:

        lnfnc = lambda x, a, b: a*x + b
        p0, c0 = _curve_fit(lnfnc, ts[:,0], ts[:,1], sigma=ts[:,2])
        ts[:,1] = ts[:,1] - lnfnc(ts[:,0], p0[0], p0[1])

        if vrbs:
            print("Linear De-trend Coefficients [a*x + b]")
            print("a:", p0[0])
            print("b:", p0[1])

    else:

        lnfnc = lambda x, a, b, c: a*x**2.0 + b*x + c
        p0, c0 = _curve_fit(lnfnc, ts[:,0], ts[:,1], sigma=ts[:,2])
        ts[:,1] = ts[:,1] - lnfnc(ts[:,0], p0[0], p0[1], p0[2])

        if vrbs:
            print("Quadratic De-trend Coefficients [a*x**2 + b*x + c]")
            print("a:", p0[0])
            print("b:", p0[1])
            print("c:", p0[2])

    return ts

def get_timeseries(infile1, infile2, vrbs, plyft):

    """
        Subroutine - get_timeseries
          Takes the user specified filenames and runs tsdtrnd and set_unitytime.
          Returns the prepared time series for DCF.
    """

    ts1_in = _loadtxt(infile1, comments='#', delimiter=',')
    ts2_in = _loadtxt(infile2, comments='#', delimiter=',')

    ts1 = chck_tserr(ts1_in)
    ts2 = chck_tserr(ts2_in)

    ts1, ts2 = set_unitytime(ts1, ts2)
    ts1 = tsdtrnd(ts1, vrbs, plyft)
    ts2 = tsdtrnd(ts2, vrbs, plyft)

    return ts1, ts2
