'''
    usage: dcf.py time_series1.dat time_series2.dat 
                  int[lag_range_low] int[lag_range_hi]
                  int[N_lag_bins]

    A simple implementation of the discrete correlation function (DCF)

'''

import numpy as np
import matplotlib.pyplot as plt
import sys
import time

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
    ts1 = lndtrnd(ts1)
    ts2 = lndtrnd(ts2)
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
    gkrn = lambda x: np.exp(-1.0 * np.abs(x)**2 / (2.0 * h**2)) / np.sqrt(2.0 * np.pi * h)
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
startTime = time.time()

INFILE1 = sys.argv[1]
INFILE2 = sys.argv[2]
INFILE2P = sys.argv[3]
LGL = float(sys.argv[4])
LGH = float(sys.argv[5])
N = int(sys.argv[6])
M = 100

print "\nTime series preparation"
TS1, TS2 = get_timeseries(INFILE1, INFILE2)
TS2P = np.loadtxt(INFILE2P, comments='!')

DT = (LGH - LGL) / float(N)
T = np.linspace(LGL+(DT/2.0), LGH-(DT/2.0), N)
print "Lag bin size:", DT

DCF, DCFERR = sdcf(TS1, TS2, T, DT)
print "Time to complete DCF:", time.time() - startTime

DCFg, DCFERRg = gdcf(TS1, TS2, T, DT)

'''
    Plots
'''

plt.figure(0)
plt.errorbar(T, DCF, DCFERR, color='k', ls='-', capsize=0)
plt.errorbar(T, DCFg, DCFERRg, color='r', ls='-', capsize=0)
#plt.plot(T, MCDCF[:,0], 'k--')
#plt.plot(T, MCDCF[:,1], 'k-.')
#plt.plot(T, MCDCF[:,2], 'k-.')
#plt.plot(T, MCDCF[:,3], 'k:')
#plt.plot(T, MCDCF[:,4], 'k:')
plt.xlim(LGL, LGH)

#plt.figure(1)
#plt.hist(MCDCF[:,31])

plt.show()
