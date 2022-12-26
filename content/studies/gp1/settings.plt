#!/usr/bin/gnuplot -persist
#  
#    	G N U P L O T
#    	Version 4.0 patchlevel 0
#
#	Standard Settings for GPI
#       (c) 2005 Michael Goerz
#       http://www.physik.fu-berlin.de/~goerz/gp1/plotsettings_en.html
#
# See http://t16web.lanl.gov/Kawano/gnuplot/index-e.html
# for a good introduction to Gnuplot
#
# remember the 'help' command


# To save the plot to a postscript file, use
set terminal postscript enhanced
set output 'out.ps'


unset key
set tics in
set ticslevel 0.5
set ticscale 1 0.5
set mxtics 10
set mytics 10
set nox2tics
set noy2tics
set fit noerrorvariables
set grid xtics mxtics ytics mytics noztics nomztics

# If you want logscale, change this to 'set'
# You can use 'logscale x', 'logscale y', 'logscale xy'
unset logscale

# If you want to, get can get rid of the right and top border axes:
# set border 3
# set xtics nomirror
# set ytics nomirror



# *************************************************************************

# This is an example for the following scenario:
# The datafile contains three blocks, separated by blank lines, each line 
# has the x value, the x error, the y value, and the y error separated by tabs
# the first block contains good data points, which will be used for the fit,
# the second block contains bad data, which will be plotted, but not used for
# the fit, and the third block contains two data points that describe the worst
# fit. The total plot will consist of the good data points, plotted as dots with
# xyerrorbars, the bad data points, plotted as circles with xyerrorbars, a best
# fit through the good data, and a worst fit, as a dashed line.
# The data is in data.csv


set title "Plot of Experiment Data"
set xlabel "xdata  /  xunit"
set ylabel "ydata  /  yunit"

# To set the plot ranges, use the following
# First look at the automatic output, then adjust manually
# set xrange [0:10]
# set yrange [0:10]


# fit
# from the first data block
f(x)=a*x+b
fit f(x) "data.csv" using 1:3 every :::0::0 via a,b

# worst fit
# from the third data block (not really a good idea, use as separate programm to
# calculate this)
e(x)=c*x+d
fit e(x) "data.csv" using 1:3 every :::2::2  via c,d
# in general, it might be better to use a separate programm to calculate best 
# fit and worst fit, and to just enter the formula into gnuplot


# see fit.log for details on the fitted parameters



plot f(x) linetype 1 linewidth 1, \
     e(x) linetype 9 linewidth 1, \
     "data.csv" every :::0::0  using 1:3:2:4 with xyerrorbars linetype 1 linewidth 1 pointtype 7 pointsize .5, \
     "data.csv" every :::1::1  using 1:3:2:4 with xyerrorbars linetype 1 linewidth 1 pointtype 6 pointsize 1



# 'with' can be lines, dots, points, linespoints, impulses, steps, boxes,
#  xerrorbars, yerrorbars, xyerrorbars, vector, ...

# To plot an interpolated line between data points, you could use
# plot "data.csv" using 1:2 notitle with points, \
#      "data.csv" using 1:2 smooth csplines \


# The syntax for every is
# every I:J:K:L:M:N 	
# I 	Line increment
# J 	Data block increment
# K 	The first line
# L 	The first data block
# M 	The last line
# N 	The last data block 
# e.g.
# every 2 		plot every 2 line
# every ::3 		skip the first 3 lines
# every ::3::5 		plot from the 4-th to 6-th lines
# every ::0::0 		plot the first line only
# every 2::::6 		plot the 1,3,5,7-th lines
# every :2 		plot every 2 data block
# every :::5::8 	plot from 5-th to 8-th data blocks
# Data blocks are separated by blank lines in the file


#    EOF
