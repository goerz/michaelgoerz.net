"""Render bibtex files in Jinja templates.

See theme/templates/bibliography.j2
"""

import bibtexparser
from bibtexparser.customization import (
    convert_to_unicode,
    author,
    editor,
    splitname,
)
from bibtexparser.bparser import BibTexParser


NAMES_TO_HIGHLIGHT = []


def process_record(record):
    """Process a raw record

    * Ensure unicode encoding of author names
    * Authors/Editors are parsed into a list of structures name objects
    """
    record = convert_to_unicode(record)
    record = author(record)
    for (i, name) in enumerate(record["author"]):
        record["author"][i] = splitname(name)
    if "editor" in record:
        record = editor(record)
        for (i, name) in enumerate(record["editor"]):
            record["editor"][i] = splitname(name)
    return record


def read_bibtex(filename):
    """Read a bibtex file.

    Return a list of records, where each record is a dict as returned by
    `process_record`.

    This is intended as a Jinja function, but must be registered with
    `register_in_templates`.
    """
    with open(filename, encoding="utf-8") as bibtex_file:
        parser = BibTexParser()
        parser.customization = process_record
        bib = bibtexparser.load(bibtex_file, parser=parser)
    return bib.entries


def join_authors(names):
    """Join author names.

    For a list of names (strings, "First Last"), join the names with comma and
    "and" for the last name.
    """
    if len(names) <= 1:
        return "".join(names)
    if len(names) == 2:
        return " and ".join(names)
    return f"{', '.join(names[:-1])}, and {names[-1]}"


def format_bib_authors(authors):
    """Format the list of authors into HTML.

    This is used as a Jinja filter in `theme/templates/bibliography.j2`, but
    must be registered with `register_in_templates`.
    """
    names = [
        (
            "{first} {von} {last} {jr}".format(
                first=" ".join(author["first"]),
                von=" ".join(author["von"]),
                last=" ".join(author["last"]),
                jr=" ".join(author["jr"]),
            )
        )
        .replace("  ", " ")
        .strip()
        for author in authors
    ]
    for (i, name) in enumerate(names):
        if name in NAMES_TO_HIGHLIGHT:
            name = f"<b>{name}</b>"
        name = name.replace(" ", "&nbsp;")
        names[i] = name
    return join_authors(names)


def format_bib_links(record):
    """Format a list of links into HTML.

    This is used as a Jinja filter in `theme/templates/bibliography.j2`, but
    must be registered with `register_in_templates`.
    """
    parts = []
    if "extra_links_first" in record:
        for line in record["extra_links_first"].strip().splitlines():
            title, link = line.split(":")
            parts.append('<a href="%s">%s</a>' % (link.strip(), title.strip()))
    if "doi" in record:
        parts.append('<a href="https://dx.doi.org/%s">DOI</a>' % record["doi"])
    if "eprint" in record:
        parts.append(
            '<a href="https://arxiv.org/abs/%s">arXiv</a>' % record["eprint"]
        )
    if "pdf" in record:
        parts.append('<a href="%s">PDF</a>' % record["pdf"])
    if "url" in record:
        parts.append('<a href="%s">Web</a>' % record["url"])
    if "youtube" in record:
        parts.append('<a href="%s">Youtube</a>' % record["youtube"])
    if "github" in record:
        parts.append('<a href="%s">Github</a>' % record["github"])
    if len(parts) > 0:
        return "[&nbsp;" + "&nbsp;|&nbsp;".join(parts) + "&nbsp;]"
    else:
        return ""


def register_in_templates(templates):
    """Register the required functions/filters into the given template manager.

    The `templates` is an instances of `src.templates.Templates`.
    """
    templates.env.globals["read_bibtex"] = read_bibtex
    templates.env.filters["format_bib_authors"] = format_bib_authors
    templates.env.filters["format_bib_links"] = format_bib_links
