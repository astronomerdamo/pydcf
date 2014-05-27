#dcf.py : A Python Implementation of the Discrete Correlation Function (DCF)

##Requirements

* Python 2.7
* Numpy
* Scipy
* Matplotlib

*Python 3 version coming shortly*

##Introduction

The Discrete Correlation Function (DCF) was developed by Edelson and Krolik, 1988, ApJ, 333, 646 for use on unevenly sampled and/or gapped data. Traditional timing analysis, ie: CCF, requires that a time series is sampled evenly in the time domain. In many real world applications obtaining perfectly sampled data may be difficult [read: damn near impossible], hence the need for a timing analysis tool designed specifically for such cases.

##Installation

`
$ git clone this_repo
`

##Usage

For complete usage:

`
$ python dcf.py -h
`

When calling dcf.py you **must** specify five pieces of information on the commands line:

* path/time_series1.dat : first time series file
* path/time_series2.dat : second time series file
* lag_range_low : low end of the range to be explored
* lag_range_high : high end of the range to be explored
* lag_bin_width : width of lag bin, dt

###Additional Settings

Optional arguments may be passed to dcf.py:

* -w=[slot, gauss] : corresponds to the weighting of the matching pairs. Default behaviour is 'slot'.
* -p=[0,1,2] : the order of the polynomial to be fit and subtracted from the time series. Default is '0'.
* -np --no-plot : By default dcf.py plots the results in a matplotlib.pyplot window, disable this by including flag.
* -o --output : By default dcf.py does not write any information to file. If you would like a plain text, space delimited output file include this flag. Spits out 'dcf_output.dat' in the current working directory.
* -v --verbose : By default dcf.py operates silently, if you are curious or a control freak use this flag.

I wish I didn't have to say this but if you choose to run dcf.py and the only optional flag you raise is '--no-plot', the program will start and finish without you, the user, seeing anything at all.

##Example

Included in this repo is example data, example/ts1.dat and example/ts2.dat. It's supposed to represent realistic data you might encounter. Both time series are taken from mysterious power law processes. You've told one of your grad students to take readings every 6 hours for a year - big mistake. Not only have they failed taking readings exactly every 6 hours, they've taken the weekend off and they disappeared for two weeks in the summer leaving a massive gap. The resulting data is unevenly sampled on short timescales, has short term small gaps and a single large long-term gap.

To search for correlation using dcf.py

`
$ python dcf.py example/ts1.dat example/ts2.dat -200 200 3.5
`

This command attempts to correlate ts1.dat and ts2.dat over a time range of +/- 200 days with a bin width of 3.5 days. Try it. See that peak at +42 days, that's a correlation.

Want more information? Maybe there is a linear trend in the data you want to get rid of and you'd like an output file as well:

`
$ python dcf.py example/ts1.dat example/ts2.dat -200 200 3.5 -v -p=1 -o
`

This spits out a bunch of information, subtracts a linear fit from the input data and writes 'dcf_output.dat' in the current working directory.

##Reference

Source Paper: [Edelson and Krolik, 1988](http://articles.adsabs.harvard.edu/full/1988ApJ...333..646E)
