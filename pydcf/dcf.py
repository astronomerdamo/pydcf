"""
    A simple implementation of the discrete correlation function (DCF)
    Author: Damien Robertson - robertsondamien@gmail.com

    Usage:
      $ python dcf.py -h for help and basic instruction

"""

from pydcf.cli import _build_cli_args, _cli_pipeline

def pydcf_cli():
    print(__doc__)
    opts = _build_cli_args()
    _cli_pipeline(opts)

def pydcf_pac():
    print("derp")

if __name__ == "__main__":
    pydcf_cli()
