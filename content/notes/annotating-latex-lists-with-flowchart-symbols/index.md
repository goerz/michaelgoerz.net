---
Category: Tech
tags: latex
Date: 06 Oct 2009
---

# Annotating LaTeX Lists with Flowchart symbols

There's a neat little trick of putting TikZ code in the place of list bullets
in LaTeX. Together with TikZ's overlay feature, I was able to make a small
graphical flowchart out of of list items: You just put a small tikzpicture in
the place of every bullet, defining some globally accessible node with the
'remember picture' option. This has to be done by defining a command for
inserting the picture, like this:

```tex
\newcommand\fcInstr[1]{{'{%'}}
  \begin{tikzpicture}[x=10pt, y=10pt, remember picture]%
    \node[coordinate] (#1) at (1,0.5) {};
    \draw (0,0) rectangle (2,1);%
  \end{tikzpicture}%
}
```

Not that the node is named after the first parameter: every node needs to have
a unique name.

You then write your list

```tex
\begin{itemize}
  \item[\fcInstr{a}] Set $t_n$: time grid for global $[0,T]$
  % ...
```

Lastly, you can add add another tikzpicture to your document in which the
defined nodes are referenced. In my example, I want to draw arrows between the
'bullet' picture.

Alltogether, it comes out like this:
* [flowchart.tex](flowchart.tex)
* [flowchart.pdf](flowchart.pdf)
