---
Date: 2018-01-14 00:01:18
Category: Programming
Tags: jupyter, latex, python
---

# Custom template for converting jupyter notebooks to latex

## The revtex template file

The file [revtex.tplx][] ([download][]) is a custom template for converting
[jupyter notebooks][1] to latex with [nbconvert][2]. Note that this is not so
much for converting a notebook into a proper article (this is best done through
markdown as an intermediary). Instead, the goal is to generate a printable pdf
of a notebook (via latex).

Compared to the default template, it has the following features:

*   Use the [`revtex` document class][3] (single column). This results in a more
    condensed and readable output

*   Support for the [`braket` package][4]

*   Fixed title block. The document will be dated. The `title`, `author`,
    and `affiliation` may be defined
    in the [notebook metadata][5]. This is based on
    [Julius Schulz' template][6]. For example you might put the following in the
    notebook metadata (`Edit → Edit Notebook Metadata`):

        "latex_metadata": {
            "author": "M H Goerz",
            "affiliation": "Stanford University",
            "title": "An example notebook",
            "bib": "notebook.bib"
        }

*   Support for hiding input cells. Technically, this looks for `hide_input`
    either in the notebook metadata (hide *all* cells), or in cell
    metadata (hide a specific cell).

    In practice, instead of editing the metadata directly, cells can be hidden
    via the "Hide input" and "Hide input all" extensions that may be installed
    through the [`jupyter_contrib_nbextensions` package][7]

*   Support for bibtex [bibliographies][8]. You can insert a citation in a
    markdown cell as e.g.

        <cite data-cite="GoerzNPJQI2017">[GoerzNPJQI2017]</cite>

    The generated tex file will then include a `\cite{GoerzNPJQI2017}` command,
    which should be defined in a file `references.bib`. An alternative bibtex
    file may be set in the notebook metadata, in `"latex_metadata" > "bib"` (see
    above)

    Alternatively, you can add a raw cell at the end of the notebook that
    contains the tex code for the bibliography, e.g.

    ```latex
    \begin{thebibliography}{9}

        \bibitem{GoerzNPJQI2017}
        Michael H. Goerz, Felix Motzoi, K. Birgitta Whaley, and Christiane P. Koch.
        npj Quant. Info. \bf{3}, 37 (2017)

    \end{thebibliography}
    ```


## Manual usage

To use the template, [download][] and store it locally, then call `nbconvert` as
e.g.

    jupyter nbconvert --to=latex --template=./revtex.tplx file.ipynb

Note that this only works if you do not set up templates in a config file (see
below). If you do, you may to use

    jupyter nbconvert --to=latex --LatexExporter.template_file=./revtex.tplx file.ipynb

instead.

Then compile the resulting file with `pdflatex`.

You can also convert directly to pdf, using

    jupyter nbconvert --to=pdf --PdfExporter.template_file=./revtex.tplx file.ipynb

Out of the box, this does not work with a bibliography file, however (because
the bib file is not copied to the temporary directory in which the compilation
happens). You can use a raw cell containing the bibliography, though.


## Setting up the template as a default

The template can be set as a default in the
[`~/.jupyter/jupyter_nbconvert_config.py` config file][9]. It should contain the
following:

```python
custom_path = os.path.expanduser("~/.jupyter/nbconvert_templates")
c.TemplateExporter.template_path.append(custom_path)
c.LatexExporter.template_file = 'revtex'
c.PDFExporter.latex_count = 3
c.PDFExporter.template_file = 'revtex'
c.PDFExporter.latex_command = ['xelatex', '{filename}']
```

The file [revtex.tplx][download] must be placed in
`~/.jupyter/nbconvert_templates/`.


## Using the template from inside the notebook interface

The notebook interface allows to directly download converted versions of the
notebook (`File → Download as`). However, the settings for this are not taken
from [`~/.jupyter/jupyter_nbconvert_config.py`][9]. Instead, the same settings
as above must be duplicated in the
[`~/.jupyter/jupyter_notebook_config.py` config file][10].


[revtex.tplx]: https://gist.github.com/goerz/d5019bedacf5956bcf03ca8683dc5217#file-revtex-tplx
[download]: https://gist.githubusercontent.com/goerz/d5019bedacf5956bcf03ca8683dc5217/raw/393f11244ef037759a19710f4d979770ac287717/revtex.tplx
[1]: http://jupyter.org
[2]: http://nbconvert.readthedocs.io/en/latest/
[3]: https://journals.aps.org/revtex
[4]: https://ctan.org/tex-archive/macros/latex/contrib/braket?lang=en
[5]: https://nbformat.readthedocs.io/en/latest/format_description.html#notebook-metadata
[6]: http://blog.juliusschulz.de/blog/ultimate-ipython-notebook#document-metadata
[7]: https://github.com/ipython-contrib/jupyter_contrib_nbextensions#jupyter-notebook-extensions
[8]: https://nbviewer.jupyter.org/github/jupyter/nbconvert-examples/blob/master/citations/Tutorial.ipynb
[9]: http://nbconvert.readthedocs.io/en/latest/config_options.html
[10]: http://jupyter-notebook.readthedocs.io/en/stable/config.html
