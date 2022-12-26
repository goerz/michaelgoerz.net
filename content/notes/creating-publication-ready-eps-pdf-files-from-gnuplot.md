---
Category: Tech
Tags: latex, gnuplot, visualization
Date: 2012-10-06 01:35:05
---

# Creating Publication-Ready EPS/PDF Files from Gnuplot

You must use a reasonably recent version of Gnuplot (>4.4).

## Layout

It is a good idea to specify line styles, e.g.

```gnuplot
set style line 1 linetype 1 linecolor 0 linewidth "3pt"
set style line 2 linetype 1 linecolor 3 linewidth "3pt"
set style line 3 linetype 1 linecolor 1 linewidth "3pt"
set style line 4 linetype 1 linecolor 2 linewidth "3pt"
set style line 5 linetype 1 linecolor 4 linewidth "3pt"
```

Always specify the exact size at which the figure will be printed when setting
the terminal. Then, place the axes on the canvas by explicitly specifying the
margins.

```gnuplot
set lmargin at screen 0.1
set bmargin at screen 0.135
set tmargin at screen 0.95
set rmargin at screen 0.95
```

See [pulse.plt](https://github.com/goerz/fortran_examples/blob/master/inout/pulse.plt)
or [pulse_multi.plt](https://github.com/goerz/fortran_examples/blob/master/inout/pulse_multi.plt)
for an example.

## Creating Encapsulated Postscript (EPS)

Example terminal for generating EPS:

```gnuplot
set term postscript eps size 7.5cm,4.7cm clip enhanced color font 'Arial' 11
```

The plot should fit exactly in the specified size, but sometimes Gnuplot screws
up the bounding box. You may have to edit the resulting postscript file:

*   Open the eps file in `gv`, from the State menu, select "Watch file"
*   Open the eps file in vim, go to the bounding box line near the top, which
    looks something like

        %%BoundingBox: 50 50 262 182

    The numbers are left, bottom, right, top, in ("big") postscript points
    (1/72 inch), measured from the bottom left of the page.

*   Edit the bounding box parameters. You may use the `units` program to do
    conversion between postscript points and cm, e.g.

        You have: (262-50) postscriptpoint
        You want: cm
                  * 7.47888888888888914152630604804
                  / 0.133709701381666906661038751736

    `gv` should show you instantaneous feedback on the bounding box

## Creating PDF

You may be able to use a pdf-terminal from gnuplot directly. Otherwise, create
an EPS file first and convert it to PDF with `epstopdf` (which is just a wrapper
around `gs`). The resulting pdf file should be cropped correctly to the
postscript bounding box. If it is not, use `pdfcrop`. Check the page size with
`pdfinfo` and possibly repeat the use of `pdfcrop` with an approprate
`--margins` option.
