'''
    A simple implementation of the discrete correlation function (DCF)

    Usage:
      $ python dcf.py -h for help

'''

import numpy as np
#import time

'''
    Subroutines
'''

def lndtrnd(ts):
    from scipy.optimize import curve_fit
    lnfnc = lambda x, a, b: a*x + b
    p0, c0 = curve_fit(lnfnc, ts[:,0], ts[:,1], sigma=ts[:,2])
    ts[:,1] = ts[:,1] - lnfnc(ts[:,0], p0[0], p0[1])
    vrbs = 0
    if vrbs == 1:
        print "Linear Detrend Coefficients"
        print "a:", p0[0]
        print "b:", p0[1]
    return ts

def set_unitytime(ts1, ts2):
    unitytime = min(np.min(ts1[:,0]), np.min(ts2[:,0]))
    ts1[:,0] = ts1[:,0] - unitytime
    ts2[:,0] = ts2[:,0] - unitytime
    return ts1, ts2

def get_timeseries(infile1, infile2):
    ts1 = np.loadtxt(infile1, comments='!')
    ts2 = np.loadtxt(infile2, comments='!')
    ts1, ts2 = set_unitytime(ts1, ts2)
    #ts1 = lndtrnd(ts1)
    #ts2 = lndtrnd(ts2)
    return ts1, ts2

def sdcf(ts1, ts2, t, dt):
    dcf = np.zeros(t.shape[0])
    dcferr = np.zeros(t.shape[0])
    n = np.zeros(t.shape[0])

    dst = np.empty((ts1.shape[0], ts2.shape[0]))
    for i in range(ts1.shape[0]):
        for j in range(ts2.shape[0]):
            dst[i,j] = ts2[j,0] - ts1[i,0]

    for k in range(t.shape[0]):
        tlo = t[k] - dt/2.0
        thi = t[k] + dt/2.0
        ts1idx, ts2idx = np.where((dst <= thi) & (dst >= tlo))

        mts2 = np.mean(ts2[ts2idx,1])
        mts1 = np.mean(ts1[ts1idx,1])
        n[k] = ts1idx.shape[0]

        dcfdnm = np.sqrt((np.var(ts1[ts1idx,1]) - np.mean(ts1[ts1idx,2])**2) \
                         * (np.var(ts2[ts2idx,1]) - np.mean(ts2[ts2idx,2])**2))

        dcfs = (ts2[ts2idx,1] - mts2) * (ts1[ts1idx,1] - mts1) / dcfdnm

        dcf[k] = np.sum(dcfs) / float(n[k])
        dcferr[k] = np.sqrt(np.sum((dcfs - dcf[k])**2)) / float(n[k] - 1)
    return dcf, dcferr

def gdcf(ts1, ts2, t, dt):
    h = dt/4.0
    gkrn = lambda x: np.exp(-1.0 * np.abs(x)**2 / (2.0 * h**2)) \
           / np.sqrt(2.0 * np.pi * h)
    cntrbt = gkrn(3.290527*h)

    dcf = np.zeros(t.shape[0])
    dcferr = np.zeros(t.shape[0])
    n = np.zeros(t.shape[0])

    dst = np.empty((ts1.shape[0], ts2.shape[0]))
    #n = ts1.shape[0] * ts2.shape[0]
    for i in range(ts1.shape[0]):
        for j in range(ts2.shape[0]):
            dst[i,j] = ts2[j,0] - ts1[i,0]

    for k in range(t.shape[0]):
        gdst = gkrn(dst - t[k])
        ts1idx, ts2idx = np.where(gdst >= cntrbt)

        mts2 = np.mean(ts2[ts2idx,1])
        mts1 = np.mean(ts1[ts1idx,1])
        n[k] = ts1idx.shape[0]

        dcfdnm = np.sqrt((np.var(ts1[ts1idx,1]) - np.mean(ts1[ts1idx,2])**2) \
                         * (np.var(ts2[ts2idx,1]) - np.mean(ts2[ts2idx,2])**2))

        dcfs = (ts2[ts2idx,1] - mts2) * (ts1[ts1idx,1] - mts1) / dcfdnm
        dcf[k] = np.sum(dcfs) / float(n[k])
        dcferr[k] = np.sqrt(np.sum((dcfs - dcf[k])**2)) / float(n[k] - 1)
    return dcf, dcferr

'''
    MAIN
'''

import argparse

INPUT = argparse.ArgumentParser(description='DCF USER PARAMETERS')

'''
    USER PARAMETER INPUT
    STANDARD PARAMETERS (REQUIRED):
        time_series1.dat - path/filename
        time_series2.dat - path/filename
        lag_range_low    - float
        lag_range_high   - float
        lag_bins         - int
'''

INPUT.add_argument('infile1', metavar='time_series1', type=file, nargs=1,
                   help='Time Series 1')
INPUT.add_argument('infile2', metavar='time_series2', type=file, nargs=1,
                   help='Time Series 2')
INPUT.add_argument('lgl', metavar='lag_range_low', type=float, nargs=1,
                   help='Lag range low')
INPUT.add_argument('lgh', metavar='lag_range_high', type=float, nargs=1,
                   help='Lag range high')
INPUT.add_argument('n', metavar='lag_bins', type=int, nargs=1,
                   help='Number of lag bins')

'''
    USER PARAMETER INPUT
    OPTIONAL PARAMETERS:
        weight   = 'slot' or 'gauss'
        polyfit  = 0, 1, 2
        plot     = True or False
'''

INPUT.add_argument('-w', '--weight', metavar='weight', type=str, nargs=1,
                   default='slot', choices=['slot', 'gauss'],
                   required=False, help='Lag bin weighting scheme')
INPUT.add_argument('-pf', '--polyfit', metavar='polyfit', type=int, nargs=1,
                   default=0, choices=[0, 1, 2],
                   required=False, help='Polynomial fit subtraction')
INPUT.add_argument('-pl', '--plotshow', metavar='plotshow', type=bool,
                   nargs=1, default=False, help='Show plot?')
INPUT.add_argument('-v', '--verbose', metavar='verbose', type=bool,
                   nargs=1, default=False, help='Show all steps')

OPTS = INPUT.parse_args()

'''
    USER PARAMETER CHECK AND READOUT
    This section will fail if:
        Parameters 'lag_range_low' and 'lag_range_high' are not symmetric
            about zero, ie: |lag_range_low| == |lag_range_high|
        Parameter 'lag_range_low' is greater than 'lag_range_high'.

    **PITFALL**
        There is no check to make sure the user enters a sensible
        number of lag bins. See README for more details.
'''

assert abs(OPTS.lgl[0]) == abs(OPTS.lgh[0]), "INPUT ERROR - LAG RANGE"
assert OPTS.lgl[0] < OPTS.lgh[0], "INPUT ERROR - LAG RANGE"

if OPTS.verbose[0]:
    print
    print "PYTHON SCRIPT: dcf"
    print
    print "INPUT TIMESERIES 1:", OPTS.infile1[0]
    print "INPUT TIMESERIES 2:", OPTS.infile2[0]
    print "LAG RANGE PROBED  :", OPTS.lgl[0], " - ", OPTS.lgh[0]
    print "NUMBER OF BINS    :", OPTS.n[0]
    print

'''
    TIME SERIES PREPERATION
    Blarg
'''
print "\nTime series preparation"
TS1, TS2 = get_timeseries(OPTS.infile1[0], OPTS.infile2[0])

'''
    DCF STEP
'''

DT = (OPTS.lgh[0] - OPTS.lgl[0]) / float(OPTS.n[0])
T = np.linspace(OPTS.lgl[0]+(DT/2.0), OPTS.lgh[0]-(DT/2.0), OPTS.n[0])
print "Lag bin size:", DT

DCF, DCFERR = sdcf(TS1, TS2, T, DT)
#print "Time to complete DCF:", time.time() - startTime

#DCFg, DCFERRg = gdcf(TS1, TS2, T, DT)

'''
    PLOT RESULTS
'''

if OPTS.plotshow[0]:
    import matplotlib.pyplot as plt
    plt.figure(0)
    plt.errorbar(T, DCF, DCFERR, color='k', ls='-', capsize=0)
    plt.xlim(OPTS.lgl[0], OPTS.lgh[0])
    plt.show()
