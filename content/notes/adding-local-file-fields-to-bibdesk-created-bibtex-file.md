---
Category: Tech
Tags: latex, mac, bibtex
Date: 25 Aug 2009
---

# Adding Local-File fields to BibDesk created BibTeX File

BibTeX files that were created with the BibDesk program on the Mac store links
to local files as smart references, which has a lot of benefits:

> To be precise, it's a base64 encoded (keyed) archived dictionary
> containing a relative path and a file alias (an alias stores a full
> path and a file ID). It is designed to support a large range of
> storage procedures, as it can find a file by relative path, absolute
> path, and file ID (in that order). This means that you can
> - move/rename the .bib file (as it stores full paths)
> - move/rename a linked file (as it stores file IDs)
> - move the .bib file and linked files together (as it stores relative
>   paths)
> - copy the .bib file and linked files togther, even between different
> machines (as it stores relative paths) [(bibdesk user mailing list)][1]

[1]: https://sourceforge.net/p/bibdesk/mailman/message/19986756/

This works perfectly as long as you stay on a Mac. However, if you have to
share the BibTeX file with someone who cannot run BibDesk, it may be useful to
add some human-readable information as well. For this, I've written a small
script that is an adaption of the code found at
<https://sourceforge.net/p/bibdesk/mailman/message/21420575/> It adds a
Local-File field to the BibTeX file with the relative path of the referenced
file.


<http://gist.github.com/goerz/5157942>

<script src="http://gist.github.com/180474.js"> </script>
