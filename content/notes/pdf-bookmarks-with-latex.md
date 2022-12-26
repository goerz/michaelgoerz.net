---
Category: Tech
Tags: pdf, latex, pdfpages, bookmarks
Date: 29 Apr 2011
---

# PDF Bookmarks with LaTeX

The combination of [pdfpages][1], [hyperref][2], and [bookmark][3] allows for a
very neat way of adding an outline to an existing pdf file. For example, we can
use the following tex file to add a (partial) outline to my [diploma
thesis][4].

[1]: http://www.ctan.org/tex-archive/macros/latex/contrib/pdfpages/
[2]: http://www.ctan.org/tex-archive/macros/latex/contrib/hyperref/
[3]: http://www.ctan.org/pkg/bookmark
[4]: /research/diploma_thesis.pdf

```latex
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{pdfpages}
\usepackage[
  pdfpagelabels=true,
  pdftitle={Optimization of a Controlled Phasegate for Ultracold Calcium Atoms in an Optical Lattice},
  pdfauthor={Michael Goerz},
]{hyperref}
\usepackage{bookmark}

\begin{document}

\pagenumbering{arabic}
\setcounter{page}{1}
\includepdf[pages=1-2]{diploma_thesis.pdf}

\pagenumbering{roman}
\setcounter{page}{1}
\includepdf[pages=3-8]{diploma_thesis.pdf}

\pagenumbering{arabic}
\setcounter{page}{1}
\includepdf[pages=9-]{diploma_thesis.pdf}

\bookmark[page=1,level=0]{Title Page}
\bookmark[page=9,level=0]{1 Introduction}
\bookmark[page=17,level=0]{2 Quantum Computation with Calcium Atoms}
    \bookmark[page=18,level=1]{2.1 Trapping of Calcium Atoms}
    \bookmark[page=20,level=1]{2.2 Internal Degrees of Freedom and Description of a Single Qubit}
    \bookmark[page=21,level=1]{2.3 Description of Two Qubits}
        \bookmark[page=22,level=2]{2.3.1 Qubit-Qubit Interaction}
\bookmark[page=23,level=2]{2.3.2 Harmonic Approximation of the Trap Potential}
        \bookmark[page=24,level=2]{2.3.3 Summary of Two-Qubit Description}
    \bookmark[page=26,level=1]{2.4 Asymptotic Description of Two Qubits}
    \bookmark[page=27,level=1]{2.5 Quantum Information Processing with Calcium}
\bookmark[page=31,level=0]{3 Numerical Tools}
\bookmark[page=47,level=0]{4 Phasegate Optimization Schemes}
\bookmark[page=65,level=0]{5 Optimization Results for the Controlled Phasegate}
\bookmark[page=87,level=0]{6 Summary and Outlook}
\bookmark[page=93,level=0]{Appendices}

\end{document}
```

Assuming that the above is stored as `thesis_with_bm.tex`, simply running
`pdflatex thesis_with_bm.tex` will create a copy `thesis_with_bm.pdf` of
`diploma_thesis.pdf` that contains the defined outline. Also, the title and
author in the pdf meta data are set, and the pages are labeled
correctly. A great way to post-process scanned documents!
