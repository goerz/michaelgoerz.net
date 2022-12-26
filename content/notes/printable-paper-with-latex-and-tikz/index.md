---
Category: Tech
Tags: latex, tikz, goodnotes
Date: 2009-07-17
Revised: 2017-04-02
---

# Printable Paper with LaTeX and TikZ

A little while ago, I played around with [TikZ](http://www.texample.net/tikz/)
to make printable paper. As it turns out, this is absolutely trivial, and with
just a few lines you can generate pretty much anything you can imagine. Here
are the examples that I generated:

#### A4 paper ####

##### Blank Paper #####

* [Lin 24 blank page with right margin](a4_lin24_blank.pdf) ([TeX](a4_lin24_blank.tex))

##### Ruled Paper #####

* [Lin 25 9mm rules with right margin](a4_lin25_lined.pdf) ([TeX](a4_lin25_lined.tex))
* [Lin 27 9mm rules with two margins](a4_lin27_lined.pdf) ([TeX](a4_lin27_lined.tex))

##### Graph Paper #####

* [Lin 22 5mm graph paper, no margins](a4_lin22_squared.pdf) ([TeX](a4_lin22_squared.tex))
* [Lin 23 5x9mm graph paper, no margins](a4_lin23_rect5x9.pdf) ([TeX](a4_lin23_rect5x9.tex))
* [Lin 26 5mm graph paper with right margin](a4_lin26_squared.pdf) ([TeX](a4_lin26_squared.tex))
* [Lin 28 5mm graph paper with two margins](a4_lin28_squared.pdf) ([TeX](a4_lin28_squared.tex))
* [Millimeter graph paper](a4_millimeter.pdf) ([TeX](a4_millimeter.tex))

##### Underlay Paper #####

* [Lin 22 5mm underlay, no margins](a4_lin22_squared_master.pdf) ([TeX](a4_lin22_squared_master.tex))
* [Lin 28 5mm underlay with two margins](a4_lin28_squared_master.pdf) ([TeX](a4_lin28_squared_master.tex))
* [Personal Correspondence](a4_personal_master.pdf) ([TeX](a4_personal_master.tex))

#### Letter size paper ####

##### Cornell Paper #####

* [Cornell blank note taking paper](letter_cornell_blank.pdf) ([TeX](letter_cornell_blank.tex))
* [Cornell college ruled note taking paper](letter_cornell_ruled.pdf) ([TeX](letter_cornell_ruled.tex))
* [Cornell ¼ inch graph note taking paper](letter_cornell_graph.pdf) ([TeX](letter_cornell_graph.tex))

##### Ruled Paper #####

* [Narrow ruled paper](letter_narrow_ruled.pdf) ([TeX](letter_narrow_ruled.tex))
* [College ruled paper](letter_college_ruled.pdf) ([TeX](letter_college_ruled.tex))
* [Wide ruled paper](letter_wide_ruled.pdf) ([TeX](letter_wide_ruled.tex))

##### Graph Paper #####

* [¼ inch graph paper with two margins](letter_inch4squared.pdf) ([TeX](letter_inch4squared.tex))
* [Millimeter graph paper](letter_millimeter.pdf) ([TeX](letter_millimeter.tex))

##### Underlay Paper #####

* [¼ inch graph underlay with two margins](letter_inch4squared_master.pdf) ([TeX](letter_inch4squared_master.tex))
* [Personal Correspondence](letter_personal_master.pdf) ([TeX](letter_personal_master.tex))

You can adapt any of these examples to your needs easily, as well as create
more complicated layouts. Anything you can find on
[http://www.printablepaper.net/](http://www.printablepaper.net/), for sure. To
compile, run the tex file through pdflatex twice.

#### Goodnotes ####

Moving beyond "printable" paper to "virtual" paper, the
[Goodnotes app](http://www.goodnotesapp.com) allows to define
[custom templates](https://goodnotes.zendesk.com/hc/en-us/articles/202167785-How-to-add-custom-templates-).
The following template was created so that for a fully zoomed out letter-sized
page on a 13 inch iPad Pro screen, the grid is exactly 5x5 mm *on screen*. This
way, I can use a physical ruler on top of the iPad screen.

* [Goodnotes letter-sized 5mm grid on iPad Pro](letter_goodnotes_cm_grid.pdf) ([TeX](letter_goodnotes_cm_grid.tex))
