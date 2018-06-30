from argparse import ArgumentParser as _AP

import matplotlib.pyplot as plt

from pydcf.correlators import sdcf, gdcf
from pydcf.utils import set_unitytime, validate_timeseries, tsdtrnd, get_timeseries

def _build_cli_args():
    input = _AP(description="DCF USER PARAMETERS")

    input.add_argument('infile1', metavar='time_series1', type=open, nargs=1,
                       help='Time Series 1')

    input.add_argument('infile2', metavar='time_series2', type=open, nargs=1,
                       help='Time Series 2')

    input.add_argument('lgl', metavar='lag_range_low', type=float, nargs=1,
                       help='Lag range low')

    input.add_argument('lgh', metavar='lag_range_high', type=float, nargs=1,
                       help='Lag range high')

    input.add_argument('dt', metavar='lag_bin_width', type=float, nargs=1,
                       help='Width of lag bin, dt')

    input.add_argument('-w', dest='weight', type=str, nargs=1,
                       default=['slot'], choices=['slot', 'gauss'],
                       required=False, help='Lag bin weighting scheme')

    input.add_argument('-p', dest='polyfit', type=int, nargs=1,
                       default=[0], choices=[0, 1, 2],
                       required=False, help='Polynomial fit subtraction')

    input.add_argument('-np', '--no-plot', dest='noplot', action='store_false',
                       help='Do not produce plot')

    input.add_argument('-o', '--output', dest='output', action='store_true',
                       help='Write output file')

    input.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                       help='Show all steps')

    return input.parse_args()

def _cli_pipeline(opts):

    #
    #   USER PARAMETER CHECK AND READOUT
    #     This section will fail if:
    #       Parameters 'lag_range_low' and 'lag_range_high' are not symmetric
    #           about zero, ie: |lag_range_low| == |lag_range_high|
    #       Parameter 'lag_range_low' is greater than 'lag_range_high'.
    #
    #   **PITFALL**
    #     There is no check to make sure the user enters a sensible
    #     lag bin width. See README for more details.
    #

    assert opts.lgl[0] < opts.lgh[0], "INPUT ERROR - LAG RANGE"

    if opts.verbose:
        print("\nPYTHON SCRIPT: dcf3")
        print()
        print("INPUT TIMESERIES 1:", opts.infile1[0].name)
        print("INPUT TIMESERIES 2:", opts.infile2[0].name)
        print("LAG RANGE PROBED  :", opts.lgl[0], " : ", opts.lgh[0])
        print("LAG BIN WIDTH     :", opts.dt[0])

    #
    #   TIME SERIES PREPARATION
    #     This section subtracts a n'th order polynomial from both input time
    #     series prior to the DCF. The user may choose:
    #       0'th order polynomial - subtracting the mean or zeroing the data.
    #       1'st order polynomial - subtracting a linear fit
    #       2'nd order polynomial - subtracting a quadratic fit
    #     The default setting is subtracting a 0'th order polynomial (the mean).
    #     This simply zeros the data and doesn't change any intrinsic qualities.
    #
    #   **PITFALL**
    #     Just because you can subtract a n'th order polynomial doesn't mean you
    #     should. The program doesn't monitor or tell you a subtraction is
    #     harmful or unnecessary.
    #
    #   **PITFALL 2**
    #     If you have subtracted your own fits from the time series, leave the
    #     default setting, 0, as is. It won't change your data.
    #

    if opts.verbose:
        print("\nTime series preparation")

    ts1, ts2 = get_timeseries(opts.infile1[0], opts.infile2[0], opts.verbose, opts.polyfit[0])

    #
    #   DCF
    #     This section earns the paycheck for the entire program - runs the DCF
    #     algorithm. The user main choose the rectangular 'slot' weighting or
    #     the gaussian 'gauss' weighting. See README for details on pair weighting.
    #
    #   The regular weighting scheme is 'slot' and also default. The 'gauss'
    #   weighting assigns higher importance to data found at the centre of
    #   the lag bin.
    #

    dt = opts.dt[0]
    n = np.around((opts.lgh[0] - opts.lgl[0]) / float(dt))
    t = np.linspace(opts.lgl[0]+(dt/2.0), opts.lgh[0]-(dt/2.0), n)

    if opts.weight[0] == 'slot':
        if opts.verbose:
            print("\nDCF INITIATED USING SLOT WEIGHTING")
        dcf, dcferr = sdcf(ts1, ts2, t, dt)
    else:
        if opts.verbose:
            print("\nDCF INITIATED USING GAUSSIAN WEIGHTING")
        dcf, dcferr = gdcf(ts1, ts2, t, dt)

    if opts.verbose:
        print("DCF COMPLETE")

    #
    #   CHECK IF OUTPUT WRITE IS TRUE
    #

    if opts.output:
        print("Writing DCF output file to: dcf_output.csv")
        np.savetxt('dcf_output.csv', np.transpose((t, dcf, dcferr)), fmt="%.6f",
                   header="LAG,DCF,DCF_ERROR", delimiter=',')

    #
    #   PLOT RESULTS
    #     If the user wishes to suppress the plot
    #     one should use the -np or --no-plot flag on the command line.
    #
    #   Requires python module matplotlib.
    #

    if opts.noplot:
        plt.figure(0)
        plt.errorbar(T, DCF, DCFERR, color='k', ls='-', capsize=0)
        plt.xlabel("Lag")
        plt.ylabel("Correlation Coefficient")
        plt.xlim(opts.lgl[0], opts.lgh[0])
        plt.show()
