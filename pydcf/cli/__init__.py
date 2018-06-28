from argparse import ArgumentParser as _AP

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
