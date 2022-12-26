"""Render Jupyter notebook files into HTML.
"""
import datetime
import pprint
import re
import shutil
from textwrap import indent
import dateutil.parser

from nbconvert.exporters import HTMLExporter
from nbconvert.preprocessors import Preprocessor
from nbformat.validator import NotebookValidationError
from traitlets.config import Config
import yaml

from .document import Document, Category, Tag
from .frontmatter import sanitize_frontmatter
from .logging import LOG


class ExtractTitleAndFrontmatter(Preprocessor):
    """Preprocessor to extract the front matter and  title from the first two
    cells of the notebook."""

    def preprocess(self, nb, resources):
        frontmatter_cell = nb.cells[0]
        if frontmatter_cell.cell_type == "raw":
            try:
                source = frontmatter_cell.source.lstrip("---\n").rstrip("\n---")
                frontmatter = {
                    key.lower(): val
                    for (key, val) in yaml.load(
                        source, Loader=yaml.CLoader
                    ).items()
                }
            except yaml.scanner.ScannerError as exc_info:
                raise IOError(
                    f"Cannot process Notebook YAML frontmatter: {exc_info}"
                ) from None
            else:
                nb.cells = nb.cells[1:]
        else:
            frontmatter = {}
        title_cell = nb.cells[0]
        if title_cell.cell_type == "markdown" and title_cell.source.startswith(
            "# "
        ):
            if "title" in frontmatter:
                LOG.warning("Ignoring existing title in frontmatter")
            frontmatter["title"] = title_cell.source[2:].strip()
            nb.cells = nb.cells[1:]
        elif "title" not in frontmatter:
            raise ValueError("Notebook does not start with a title")
        resources["frontmatter"] = frontmatter
        return nb, resources


def render_ipynb(file, outdir, folder, data, templates):
    """Render Jupyter notebook `file` into `outdir`/`folder`."""
    if file.name == "index.ipynb":
        outfolder = outdir / folder
    else:
        outfolder = (outdir / folder / file.name).with_suffix("")
    outfolder.mkdir(parents=True, exist_ok=True)
    outfile = outfolder / "index.html"
    LOG.info("Writing html rendered from %r to %r", str(file), str(outfile))
    try:
        config = Config()
        config.HTMLExporter.preprocessors = [
            "nbconvert.preprocessors.ExtractOutputPreprocessor",
            ExtractTitleAndFrontmatter,
        ]
        try:
            html_content, resources = HTMLExporter(
                config=config, template_file="basic/index.html.j2"
            ).from_filename(file)
        except NotebookValidationError as exc_info:
            raise IOError(f"Invalid notebook {file}: {exc_info}") from None
        frontmatter = sanitize_frontmatter(file, resources["frontmatter"])
        if Tag("notebook") not in frontmatter["tags"]:
            frontmatter["tags"].append(Tag("notebook"))
        LOG.debug(
            "Frontmatter in %s:\n%s",
            str(file),
            pprint.pformat(frontmatter, indent=4),
        )
    except ValueError as exc_info:
        raise IOError(f"Error converting {file}: {exc_info}") from None
    content = html_content
    LOG.debug(
        "Rendered content in %r:\n%s",
        str(file),
        indent(content, "    ").rstrip(),
    )
    document = Document(
        file=file,
        outfile=outfile,
        category=Category("Misc"),
        section="Notes",
        content=content,
        url=str(outfolder.relative_to(outdir)),
        template=templates.default_for(file, "note.html"),
    )
    document.update(frontmatter)
    if document.title is None:
        raise IOError(f"{file} has no title")
    if not isinstance(document.category, Category):
        document.category = Category(document.category)
    template = templates[document.template]
    html_text = template.render(page=document, **data)
    outfile.write_text(html_text)
    for (filename, imgdata) in resources["outputs"].items():
        LOG.info("Writing output file %r from %r", str(filename), str(file))
        with (outfolder / filename).open("wb") as out_fh:
            out_fh.write(imgdata)
    LOG.info(
        "Copying original notebook %r to output folder %r",
        str(file),
        str(outfolder),
    )
    shutil.copy(file, outfolder)
    return document
