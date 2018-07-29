import numpy as np

def sdcf(ts1, ts2, t, dt):

    """
        Subroutine - sdcf
          DCF algorithm with slot weighting
    """

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
        ts1idx, ts2idx = np.where((dst < thi) & (dst > tlo))
        
        mts2 = np.mean(ts2[ts2idx,1])
        mts1 = np.mean(ts1[ts1idx,1])
        n[k] = ts1idx.shape[0]
        
        dcfdnm = np.sqrt((np.var(ts1[ts1idx,1]) - np.mean(ts1[ts1idx,2])**2) \
                         * (np.var(ts2[ts2idx,1]) - np.mean(ts2[ts2idx,2])**2))

        dcfs = (ts2[ts2idx,1] - mts2) * (ts1[ts1idx,1] - mts1) / dcfdnm

        dcf[k] = np.sum(dcfs) / float(n[k])
        dcferr[k] = np.sqrt(np.sum((dcfs - dcf[k])**2)) / float(n[k] - 1)

    return dcf, dcferr
