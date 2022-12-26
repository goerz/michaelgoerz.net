---
Date: 2017-04-29 13:14:32
Revised: 2018-03-14
Category: Tech
Tags: bash, latex, pdf
---

# PDF Tricks and Tips

The following is a lists of lesser known command line tools for some common
tasks in working with pdf files, in particular for preparing graphics for
inclusion in latex documents and processing scanned documents.

* **Show information about raster images embedded in pdf**

    The [poppler][] package provides the `pdfimages` utility.

        pdfimages -list <pdffile>

    shows a summary of all embedded images including their color space and
    compression algorithm. For scanned documents, we can check whether they have
    been optimally compressed. The `pdfimages` utility also allows to extract all
    images.


* **Show information about pages sizes**

    When all pages in the pdf have different (print) page sizes, the [Imagemagick][] `identify` utility can extract them:

        identify -verbose <pdffile>  | grep 'Print size'

    The result will be in inches. If you only want to know the size of the first page, the `pdfinfo` utility (part of the xpdf package) will display that (in postscript points).


* **Extract Font Information**

    The [`pdfminer` Python package][pdfminer] includes
    the `pdf2txt.py` utility.

        pdf2txt.py -p <pagenumber> -t xml <pdffile>

    shows the font and font size for all text in the pdf. This is especially useful
    if you need to create a figure that exactly matches the text of some existing
    pdf. For example, when calling `pdf2txt.py` on a pdf created with [Beamer][], we may
    find the following for some letter of the main text:

        <text font="KJEDUA+CMSS12" bbox="120.915,193.920,126.118,205.983" size="12.063">e</text>

    This indicates that the Computer-Modern-Sans-Serif-12 font is used, and by
    installing the [OTF version of the LaTeX fonts][texfonts] on your system, you
    can create a matching figure e.g. in [OmniGraffle][].



* **Rastering PDFs**

    [Imagemagick][] contains the `convert` utility to convert between various raster
    image formats, including PDF.


        convert -compress Zip -density 200 <inpdf> <outpdf>

    converts a (vector) pdf into a 200 DPI raster compressed pdf.
    The [Goodnotes][] app exports handwritten notes to PDF in a pure vector format
    that is rather large. Rastering it as above compresses the file significantly
    (but also gets rid of the OCR layer). The resulting file can be further
    compressed through the "Optimize Scanned PDF" in Adobe Acrobat.

[poppler]: https://poppler.freedesktop.org
[pdfminer]: https://github.com/pdfminer/pdfminer.six
[Beamer]: https://www.ctan.org/pkg/beamer?lang=en
[texfonts]: http://www.ctan.org/tex-archive/fonts/cm/ps-type1/bakoma/otf/
[OmniGraffle]: https://www.omnigroup.com/omnigraffle
[Imagemagick]: http://imagemagick.org/script/index.php
[Goodnotes]: http://www.goodnotesapp.com
