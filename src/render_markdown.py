"""Render markdown files into HTML.

Markdown parsing is done with [markdown-it](https://github.com/executablebooks/markdown-it-py)
"""
import datetime
import pprint
import re
from textwrap import indent
import dateutil.parser

import pygments
import yaml

from markdown_it import MarkdownIt
from markdown_it.common.utils import escapeHtml
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.container import container_plugin
from mdit_py_plugins.attrs import attrs_plugin
from mdit_py_plugins.admon import admon_plugin
from mdit_py_plugins.anchors import anchors_plugin

from .document import Document, Category
from .frontmatter import sanitize_frontmatter
from .get_history import get_history
from .logging import LOG
from .custom_renderer import CustomRenderer
from .mdmath import mdmath_plugin


def myhighlight(content, lang, attrs):
    return content


def highlight_code(code, name, attrs):
    """Highlight a block of code"""

    if attrs:
        LOG.warn(f"Ignoring {attrs=}")

    if name == "":
        return f"<pre>{code}</pre>"

    if name == "math":
        return f'<div class="math-block">$$\n{escapeHtml(code)}$$</div>\n'

    lexer = pygments.lexers.get_lexer_by_name(name)
    formatter = pygments.formatters.HtmlFormatter()

    formatted = pygments.highlight(code, lexer, formatter)
    LOG.debug(
        "name=%r, attrs=%r, code:\n%s\n⇒\n%s",
        name,
        attrs,
        indent(code, "    ").rstrip(),
        indent(formatted, "    ").rstrip(),
    )
    return formatted


PARSER = (
    MarkdownIt(
        "gfm-like",
        {
            "linkify": True,
            "html": True,
            "typographer": True,
            "highlight": highlight_code,
            "langPrefix": "",
        },
        renderer_cls=CustomRenderer,
    )
    .use(mdmath_plugin)
    .use(admon_plugin)
    .use(attrs_plugin)
    .use(anchors_plugin, min_level=1, max_level=4)
    .use(front_matter_plugin)
)


def extract_title(tokens):
    """Extract a title from the given markdown tokens.

    This looks for an h1-heading at the beginning of the given tokens. If
    found, return a tuple `(title, tokens)`, where `title` is the title text
    and `tokens` is the `tokens` with the title stripped out. If no title is
    found, return `(None, tokens)`.

    Any frontmatter in the first token is always stripped out.
    """
    try:
        has_front_matter = int(tokens[0].type == "front_matter")
        first_token = tokens[has_front_matter]
        if first_token.type == "heading_open" and first_token.tag == "h1":
            title = tokens[has_front_matter + 1].content
            return title, tokens[(has_front_matter + 3) :]
        else:
            return None, tokens[has_front_matter:]
    except IndexError:
        return None, tokens


def render_md(file, outdir, folder, data, templates):
    """Render markdown `file` into `outdir`/`folder`."""
    outfile = (outdir / folder / file.name).with_suffix(".html")
    LOG.info(
        "Writing html rendered from markdown %r to %r", str(file), str(outfile)
    )
    tokens = PARSER.parse(file.read_text())
    frontmatter = {}
    if tokens[0].type == "front_matter":
        try:
            frontmatter = sanitize_frontmatter(
                file, yaml.load(tokens[0].content, Loader=yaml.CLoader)
            )
            LOG.debug(
                "Frontmatter in %s:\n%s",
                str(file),
                pprint.pformat(frontmatter, indent=4),
            )
        except yaml.scanner.ScannerError as exc_info:
            raise IOError(
                f"Cannot process YAML frontmatter in {file}: {exc_info}"
            ) from None
    title, tokens = extract_title(tokens)
    content = PARSER.renderer.render(tokens, PARSER.options, {})
    if frontmatter.get("jinja", False):
        content = templates.from_string(content).render(**data)
    LOG.debug(
        "Rendered content in %r:\n%s",
        str(file),
        indent(content, "    ").rstrip(),
    )
    document = Document(
        title=title,
        file=file,
        outfile=outfile,
        url=str(outfile.relative_to(outdir)),
        # og_image="", # TODO
        category=Category("Misc"),
        section="Notes",
        content=content,
        template=templates.default_for(file, "page.html"),
    )
    document.update(frontmatter)
    if document.title is None:
        raise IOError(f"{file} has no title")
    template = templates[document.template]
    html_text = template.render(page=document, **data)
    outfile.write_text(html_text)
    return document
