---
Date: 2012-10-06 02:04:17
Category: Tech
Tags: latex, tikz, visualization
---

# Creating EPS files from TikZ

Since tikz files are usually not accepted when submitting publications, it is
necessary to create a standalone EPS or PDF file. That is, the `tikzpicture`
should be embedded in a complete `.tex` file, which compiles into a correctly
cropped picture, ready for inclusion with `\includegraphics`. The `.tex` file
can be easily set up to mimic the environment of the main document, so that e.g.
the fonts match.

## Using the Preview Package

Option 1 is to use the preview package.

```latex
\documentclass[a4paper,10pt]{article}

\usepackage{tikz}
\usepackage[psfixbb,graphics,tightpage,active]{preview}

\PreviewEnvironment{tikzpicture}

\begin{document}

\begin{tikzpicture}
 % ...
\end{tikzpicture}

\end{document}
```

This works especially well when using `pdflatex`. It also works flawlessly with
non-standard sizes, e.g. beamer slides or A0 posters. With "old" latex
(producing DVI, which is then converted to postscript using `dvips`), this
method has substantial problems. For one thing, all recent versions of TexLive
have a bug in the postscript they produce. This can be fixed by replacing
the line

```latex
\def\pgf@sys@postscript@header#1{\pgfutil@insertatbegincurrentpage{\special{!#1}}}
```

with

```latex
\def\pgf@sys@postscript@header#1{\AtBeginDvi{\special{! #1}}}
```

in `./tex/generic/pgf/systemlayer/pgfsys-dvips.def` inside the TexLive folder.

Even then, it does not seem possible to end up with an eps file that works as
expected (the bounding box seems broken in very mysterious ways)


## Using Externalization

Option 2 is the externalization feature that's included in pgf itself.

```latex
\documentclass[a4paper,10pt]{article}
\usepackage{tikz}
\pgfrealjobname{levels_ext}

\begin{document}

\beginpgfgraphicnamed{levels}
\begin{tikzpicture}
    % ...
\end{tikzpicture}
\endpgfgraphicnamed

\end{document}
```

This method works equally well for `pdflatex` and just `latex`. However, I've
seen it break for externalizing pictures from A0 posters. In this example, the
file must be named `levels_ext.tex`. To obtain the file `levels.dvi`, we must
compile the tex-file with the command

```shell
latex --jobname=levels levels_ext.tex
```

To go from the dvi file to an eps file, simply use `dvips -o levels.eps
levels.dvi`. Do not give the `-E` flag to `dvips`: Even without it, the
resulting postscript file will be in eps format (have a bounding box), but with
it, the resulting file actually has bounding box problems.

If `pdflatex` instead of `latex` is used, a pdf file instead of a dvi file is
generated.
