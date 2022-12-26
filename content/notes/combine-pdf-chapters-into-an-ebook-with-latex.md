---
Date: 2011-06-11 01:55:23
Category: Tech
Tags: pdf, latex, pdfpages, bookmarks
---

# Combine PDF Chapters into an Ebook with LaTeX

If you have some book chapters as individual PDF files, and would like to
combine them into a single file, with proper meta-data and bookmarks, you can
use the `pdfpages` package in LaTeX to do so:

```latex
% Example for chapters downloaded from SpringerLink
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{pdfpages}
\usepackage{hyperref}
\hypersetup{
unicode=true,
pdfpagelabels=true,
pdftitle={Atome, Molek\"ule und optische Physik 1},
pdfauthor={Ingolf V. Hertel, Claus-Peter Schulz},
}

\begin{document}


\pagenumbering{roman}

\setcounter{page}{1}
\includepdf[
addtotoc={1,section,1,Front Matter,frontmatter,
        4,section,1,Inhalt,contents},
pages=-]{front-matter.pdf}

\pagenumbering{arabic}

\setcounter{page}{1}
\includepdf[
addtotoc={1,section,1,1 Grundlagen,ch1},
pages=-]{ch01_1-46.pdf}

\setcounter{page}{47}
\includepdf[
addtotoc={1,section,1,2 Elemente der Quantenmechanik und das H-Atom,ch2},
pages=-]{ch02_47-83.pdf}

\setcounter{page}{85}
\includepdf[
addtotoc={1,section,1,3 Periodensystem und Aufhebung der L-Entartung,ch3},
pages=-]{ch03_85-106.pdf}

\setcounter{page}{107}
\includepdf[
addtotoc={1,section,1,4 Nicht stationäre Probleme: Dipolanregung,ch4},
pages=-]{ch04_107-156.pdf}

\setcounter{page}{157}
\includepdf[
addtotoc={1,section,1,{5 Linienbreiten, Multiphotonenprozesse und mehr},ch5},
pages=-]{ch05_157-193.pdf}

\setcounter{page}{195}
\includepdf[
addtotoc={1,section,1,6 Feinstruktur und Lamb-Shift,ch6},
pages=-]{ch06_159-249.pdf}

\setcounter{page}{251}
\includepdf[
addtotoc={1,section,1,7 Helium und He-artige Ionen,ch7},
pages=-]{ch07_251-280.pdf}

\setcounter{page}{281}
\includepdf[
addtotoc={1,section,1,8 Atome in externen Feldern,ch8},
pages=-]{ch08_281-345.pdf}

\setcounter{page}{347}
\includepdf[
addtotoc={1,section,1,9 Hyperfeinstruktur,ch9},
pages=-]{ch09_347-389.pdf}

\setcounter{page}{391}
\includepdf[
addtotoc={1,section,1,10 Vielelektronenatome,ch10},
pages=-]{ch10_391-434.pdf}

\setcounter{page}{435}
\includepdf[
addtotoc={1,section,1,Anhang,backmatter},
pages=-]{bm_435-511.pdf}

\end{document}
```
