---
Category: Tech
Tags: visualization, tikz
Date: 24 Jan 2010
---

# Creating Combined tikz/png Plots

In order to create truly high quality plots, you can have gnuplot write tikz
files. Wheres the latest CVS development version of gnuplot have the tikz
terminal included, I'm still using the [patch by Peter Hedwig for gnuplot
4.2](http://peter.affenbande.org/gnuplot/).

Generating tikz code from gnuplot works very nicely for "standard" plots, but
can be problematic for others. If the plot contains a lot of points, the
resulting tikz file can be hundreds of megabyte in side, and the resulting pdf
will constipate your pdf reader, if you get it to compile at all. In fact, you
run into the same problem if you use the pdf or postscript terminal in gnuplot
directly.

Another type of plot where this tends to happen is [3D color
maps](http://t16web.lanl.gov/Kawano/gnuplot/plotpm3d-e.html). The result in
tikz is thousands of small colored squares, each of to be rendered as
vector graphics.

Is there any way to make these plots manageable, while keeping the high quality
of tikz output in place? A possible solution is to combine a bitmapped plot
with vector-graphics decorations (axes, legend, etc.). To do this, we let
gnuplot generate the same plot twice: once with the tikz terminal, and once
with the png terminal, but without any axes, labels, etc. We then modify the
tikz output and delete all the parts for the actual plot, and insert the png
image in their place. This means we have the png image, and everything else
drawn on top of it with tikz.

Let's look at this in practice.

Suppose I have a [huge data file](wig.bz2) of a [Wigner
plot](http://en.wikipedia.org/wiki/Wigner_quasi-probability_distribution) that
I want to visualize as a color map. I use the following gnuplot file:

```gnuplot
set term lua plotsize 8cm,6cm font " \\tiny "
set out "wigner.tikz"

set pm3d map
set palette defined (-0.0015 "blue", 0 "white", 0.0015 "red")

splot "wig" u 1:2:3

set term png size 800,600
set out "wigner.png"

set lmargin at screen 0
set rmargin at screen 1.0
set bmargin at screen 0
set tmargin at screen 1.0

unset tics
unset border

splot "wig" u 1:2:3
```

We can see that the tikz plot is create first, then the png plot. With those
settings, the png file contains just the actual plot area without any margins
whatsoever. It looks like this:
[wigner.png](wigner.png)

The tikz file that comes out of this has some 150 MB. However, if we open it up
in a text editor, we can easily identify its structure, and write a small
script that replaces the actual plot with the png file:

[combine_pm3dmap.pl](https://gist.github.com/goerz/d2678065e570e9712584)

The second thing this script does is to make the plot legend look quite a bit
nicer. In the original, the legend was just a bunch of colored boxes stacked on
top of each other to create a fake gradient, which looks horrible. We replace
this with two true gradients, which works because we set the colors in the
gnuplot script to go from blue to white to red. So we can have one true
gradient from blue to white, and one from white to red.

Of course, the script is not really general, but I think it should work for any
pm3d map plot that uses a three-color gradient centered around white as the
palette. Also, if it's just for a single plot, you could just as easily do this
by hand.

After processing the tikz file by calling `./combine_pm3dmap.pl wigner.tikz
wigner.png`, we get this modified tikz file that is only 4.8 KB in size:

[wigner.tikz](wigner.tikz)

It can be easily compiled (e.g with the
[tikz2pdf](http://kogs-www.informatik.uni-hamburg.de/~meine/tikz/process/#tikz2pdf)
script, and don't forget to include
[gnuplot-lua-tikz.sty](http://peter.affenbande.org/gnuplot/)), resulting in the
following pdf:

[wigner.pdf](wigner.pdf)
