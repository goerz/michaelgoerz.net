---
Date: 2015-02-04 21:13:33
Category: Tech
Tags: xmgrace, visualization
---

# Colors for XMGrace

Here is a 16 color palette for [XMGrace][] that looks significantly more
pleasant than the default colors:

    @map color 0 to (255, 255, 255), "white"
    @map color 1 to (0, 0, 0), "black"
    @map color 2 to (228, 26, 28), "red"
    @map color 3 to (55, 126, 184), "blue"
    @map color 4 to (77, 175, 74), "green"
    @map color 5 to (152, 78, 163), "purple"
    @map color 6 to (255, 127, 0), "orange"
    @map color 7 to (255, 255, 51), "yellow"
    @map color 8 to (166, 86, 40), "brown"
    @map color 9 to (247, 129, 191), "pink"
    @map color 10 to (153, 153, 153), "grey"
    @map color 11 to (166, 206, 227), "lightblue"
    @map color 12 to (178, 223, 138), "lightgreen"
    @map color 13 to (251, 154, 153), "lightred"
    @map color 14 to (253, 191, 111), "lightorange"
    @map color 15 to (202, 178, 214), "lightpurple"

The colors are vaguely based on on the [Colorbrewer][] schemes. To use them, you
must open the `agr` file in a text editor and replace the color map lines with
the ones above. You might also put them inside your
`~/.grace/templates/Default.agr` file.


[XMGrace]: http://plasma-gate.weizmann.ac.il/Grace/
[Colorbrewer]: http://colorbrewer2.org
