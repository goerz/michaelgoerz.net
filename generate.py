"""
Usage:

    python generate.py [FLAGS]

Without FLAGS, generate the website for publishing and exit.

FLAGS can be the following:


    --help          Show this help

    --preview       Generate the website in "preview mode". Serve the result in
                    on port 8000 and watch for modifications, regenerating as
                    necessary.
"""

import asyncio
import logging
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

from dulwich.repo import Repo
import dulwich.porcelain as git


from src.logging import LOG
from src.templates import Templates
from src.render_markdown import render_md
from src.render_notebook import render_ipynb
from src.document import Document
import src.bibliography
import conf as CONF
import conf_publish as CONF_PUBLISH


SOURCEDIR = Path("./content")
OUTDIR = Path("./output")
THEME = Path("./theme")
REPO = Repo("./")


def collect(sourcedir):
    """Collect all the files in `sourcedir`."""
    files = []
    for file in sourcedir.rglob("*"):
        if not file.is_file():
            continue
        files.append(str(file))
    ignores = set(git.check_ignore(REPO, files))
    LOG.debug("Ignored files:\n    %s", "\n    ".join(sorted(ignores)))
    files = sorted(set(files) - ignores)
    LOG.info("Collected files:\n    %s", "\n    ".join(files))
    return [Path(file) for file in files]


async def render(file, data, templates, preview=False):
    """Render the given `file` into `OUTDIR`."""
    renderers = {
        ".md": render_md,
        ".ipynb": render_ipynb,
    }
    renderer = renderers.get(file.suffix, render_verbatim)
    folder = file.relative_to(SOURCEDIR).parent
    (OUTDIR / folder).mkdir(parents=True, exist_ok=True)
    LOG.info("Render %r into %r", str(file), str(OUTDIR / folder))
    document = renderer(file, OUTDIR, folder, data, templates)
    if preview and not document.static:
        while True:
            if not document.up_to_date:
                LOG.info(
                    "%r changed. Regenerate %r",
                    str(file),
                    str(document.outfile),
                )
                renderer(file, OUTDIR, folder, data, templates)
            await asyncio.sleep(1)
    return document


def render_verbatim(file, outdir, folder, data, templates):
    """Render `file` by copying it into `outdir`/`folder`."""
    shutil.copy(file, outdir / folder)
    outfile = outdir / folder / file.name
    return Document(file=file, outfile=outfile, static=True)


def copy_theme():
    """Copy theme static resources to output directory"""
    src = THEME / "static"
    dst = OUTDIR / "theme"
    if dst.is_dir():
        LOG.info("Skip copying %s: %s already exists", src, dst)
    else:
        LOG.info("Copy %s to %s", src, dst)
        shutil.copytree(src, dst)


async def main(preview=False):
    """Main function."""

    LOG.info("Generating website")

    files = collect(Path(SOURCEDIR))

    rx_key = re.compile("[A-Z_]+")
    data = {
        key: val for (key, val) in CONF.__dict__.items() if rx_key.match(key)
    }
    if not preview:
        data.update(
            {
                key: val
                for (key, val) in CONF_PUBLISH.__dict__.items()
                if rx_key.match(key)
            }
        )
    templates = Templates(THEME, defaults=CONF.DEFAULT_TEMPLATES)
    src.bibliography.NAMES_TO_HIGHLIGHT = CONF.BIB_NAMES_TO_HIGHLIGHT
    src.bibliography.register_in_templates(templates)

    copy_theme()

    LOG.info("#### Pass 1")
    tasks = []
    for file in files:
        tasks.append(
            asyncio.create_task(render(file, data, templates, preview=False))
        )
    documents = [await task for task in tasks]

    def is_note(document):
        return (
            (document.file.is_relative_to(Path("content") / "notes"))
            and (document.file.suffix in [".md", ".ipynb"])
            and (document.file != Path("content") / "notes" / "index.md")
        )

    data["notes"] = [document for document in documents if is_note(document)]
    LOG.debug('Collected "notes":\n%s', [d.file for d in data["notes"]])
    tags = defaultdict(list)
    categories = defaultdict(list)
    for document in documents:
        if is_note(document):
            categories[document.category].append(document)
            for tag in document.tags:
                tags[tag].append(document)
    data["categories"] = categories
    data["tags"] = tags
    LOG.debug(
        "Collected categories: %s", ", ".join(str(k) for k in categories.keys())
    )
    LOG.debug("Collected tags: %s", ", ".join(str(k) for k in tags.keys()))

    LOG.info("#### Pass 2")
    tasks = []
    for document in documents:
        if document.static:
            continue
        tasks.append(
            asyncio.create_task(
                render(document.file, data, templates, preview=preview)
            )
        )
    if preview:
        server_task = asyncio.create_subprocess_exec(
            sys.executable, "-m", "http.server", "--directory", str(OUTDIR)
        )
        await server_task
    else:
        redirects = []
        redirects.extend(CONF.REDIRECTS)
        redirects.extend(CONF_PUBLISH.REDIRECTS)
        for (file, redirect_url) in redirects:
            LOG.info("Write redirect %r -> %r", file, redirect_url)
            with open(OUTDIR / file, "w", encoding="utf8") as out_fh:
                out_fh.write(
                    templates["redirect.html"].render(
                        page=Document(file=None, outfile=file),
                        url=redirect_url,
                        **data
                    )
                )

    for task in tasks:
        await task

    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if "--debug" in sys.argv:
        LOG.setLevel(logging.DEBUG)
    if "--debug-all" in sys.argv:
        logging.getLogger().setLevel(logging.DEBUG)
        LOG.setLevel(logging.DEBUG)
    if "--help" in sys.argv:
        print(__doc__)
        sys.exit(0)
    preview = "--preview" in sys.argv
    try:
        sys.exit(asyncio.run(main(preview=preview)))
    except KeyboardInterrupt:
        pass
