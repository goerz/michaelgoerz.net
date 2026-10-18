# Sources for michaelgoerz.net

[![Build](https://github.com/goerz/michaelgoerz.net/actions/workflows/build.yml/badge.svg)](https://github.com/goerz/michaelgoerz.net/actions/workflows/build.yml)

This repository contains the source files and code to generate the website <https://michaelgoerz.net>


## Getting Started

The build environment is managed with [uv](https://docs.astral.sh/uv/), which must be installed. Python and all dependencies are pinned in `.python-version` and `uv.lock`; `make` targets run through `uv run`, which sets up the environment in `.venv` automatically.

Run `make preview` to generate the website locally and run a local web server on port 8000 to view it at <http://localhost:8000>.

This will watch all files for changes and re-generate them if necessary. This does not extend to *new* files that were generated since the server started running.

Run just `make` to see more options.


## Static Site Generation

The site is built by a small custom static site generator: `generate.py` and the modules in `src/`. It borrows the names of many settings from [Pelican](https://getpelican.com), but does not use it.

Running `make generate` (or `uv run python generate.py`) does the following:

1. Collect every file in `content/` that is not ignored by `.gitignore`. Untracked files are included, so a work-in-progress note shows up in the local preview. Only committed files end up on the server, since the server is updated from a fresh checkout (see [Deployment](#deployment)).
2. Copy `theme/static/` to `output/theme/`.
3. Render every file into `output/`, at the same relative path. Markdown (`.md`) and Jupyter notebook (`.ipynb`) files are converted to HTML through the Jinja templates in `theme/templates/`. All other files (images, PDFs, TeX sources, …) are copied verbatim.
4. Render all Markdown and notebook files a second time. The first pass collects the metadata of all notes, so that the second pass can make the `notes`, `tags`, and `categories` variables available to templates that list them.
5. Write the redirect pages listed in `REDIRECTS` (publishing mode only).

All upper-case names defined in `conf.py` become template variables. When generating for publishing (`make generate`), the settings in `conf_publish.py` are applied on top; most importantly, these set the absolute `SITEURL` and the `REDIRECTS`. The preview (`make preview`) uses only `conf.py`, with an empty `SITEURL`, so that all links point to the local server.

`THEME_VERSION` in `conf.py` is a hash of all files in `theme/static/`. It is appended as `?v=…` to the URLs of the CSS and JavaScript files, so that browsers and the CDN in front of the server fetch new versions of these files whenever they change.

The generator reads the git history of each source file with [dulwich](https://www.dulwich.io). A page with more than one commit shows a "History" link to the commit log for that file on GitHub (`HISTORY` in `conf.py`).

### Markdown Format

Markdown files are parsed with [markdown-it-py](https://markdown-it-py.readthedocs.io) in its "gfm-like" mode, which supports tables and strikethrough, converts bare URLs to links, passes raw HTML through, and replaces quotes and dashes with their typographic forms. On top of that, the following extensions are enabled:

* Admonitions (`!!! note`), via [`mdit_py_plugins.admon`](https://mdit-py-plugins.readthedocs.io/en/latest/#admonitions)
* Attributes like `{.class #id}` after an element, via [`mdit_py_plugins.attrs`](https://mdit-py-plugins.readthedocs.io/en/latest/#attributes)
* Anchors (`id` attributes) on all headings of level 1 to 4
* Math: inline as `$…$`, display as `$$…$$` or as a fenced code block with the language `math`. The math is protected from Markdown processing (`src/mdmath.py`) and rendered in the browser by [MathJax](https://www.mathjax.org) (`MATHJAX_SCRIPT` in `conf.py`).
* Syntax highlighting of fenced code blocks with [Pygments](https://pygments.org), based on the language name after the opening fence. A code block without a language name is rendered as plain `<pre>`. The highlighting uses the `friendly` style in light mode and `github-dark` in dark mode (`PYGMENTS_STYLE` and `PYGMENTS_STYLE_DARK` in `conf.py`).

A file may start with YAML front matter between two `---` lines. The keys are case-insensitive. For example:

```
---
Date: 2023-11-12
Revised: 2024-02-01
Category: Tech
Tags: make, python, julia
---

# Self-Documenting (GNU) Makefiles
```

A level-1 heading at the very top of the file (after the front matter) becomes the page title and is removed from the body; a `Title` key in the front matter takes precedence. A file without either is an error. The other recognized keys are:

| Key        | Meaning                                                                                                   |
|------------|-----------------------------------------------------------------------------------------------------------|
| `Date`     | Publication date. Without it, the date of the most recent commit of the file is used (or the current time, for an uncommitted file). |
| `Revised`  | Date of the last substantial revision, shown next to the publication date                                 |
| `Category` | A single category (default: "Misc")                                                                       |
| `Tags`     | A comma-separated string or a YAML list                                                                   |
| `Section`  | The entry of the navigation bar (`MENUITEMS` in `conf.py`) to highlight (default: "Notes")               |
| `Template` | The template in `theme/templates/` to use (see below)                                                     |
| `Jinja`    | If `True`, process the rendered HTML as a Jinja template before inserting it into the page template       |
| `exturl`   | For a note that lives elsewhere (e.g., a GitHub gist): the page only links to this URL, and the Notes index links to it directly |
| `Summary`  | Used for the `description` meta tag                                                                       |
| `Wide`     | For `page.html`: don't restrict the content to the narrow prose width                                     |

Any key is available in the template as `page.<key>` (lowercase), so a template can define additional keys.

The template defaults to `note.html` for files in `content/notes/` and to `page.html` everywhere else (`DEFAULT_TEMPLATES` in `conf.py`). The other templates are used for specific pages:

* `profile.html` for the Research page (`content/index.md`). The `Bibliography` key lists pairs of section headings and BibTeX files, which are rendered with the `bibliography` macro in `theme/templates/bibliography.j2` (code in `src/bibliography.py`). The macro handles the entry types `article`, `inproceedings`, `conference`, `phdthesis`, and `mastersthesis`. Beyond the standard fields, it uses `icon` (a logo shown next to the entry), `comment`, and the link fields `pdf`, `github`, `youtube`, `video`, and `extra_links_first` (lines of `title: url`). Links to files on the website, like `pdf` and `icon`, are relative to the root of the site. The names in `BIB_NAMES_TO_HIGHLIGHT` are set in bold.
* `projects.html` for the Programming page (`content/programming/index.md`), which reads the YAML file given in the `Projects` key. The format is documented at the top of `content/programming/projects.yml`.
* `refcards.html` for the Refcards page (`content/refcards/index.md`), which reads the YAML file given in the `Refcards` key. The format is documented at the top of `content/refcards/refcards.yml`.

A Markdown file `foo.md` is rendered to `foo.html` in the corresponding folder of `output/`. A note that has attached files (images, PDFs, …) should go into its own folder as `content/notes/<slug>/index.md`, next to its attachments, which can then be linked with relative paths. Its URL is `notes/<slug>/`.

Every Markdown or notebook file in `content/notes/` (except `content/notes/index.md`) counts as a note. The Notes index, the Tags page, and the Categories page (`content/notes/index.md`, `content/tags.md`, and `content/categories.md`) are Markdown files with `Jinja: True` that loop over the `notes`, `tags`, and `categories` variables.

There is no "draft" status. A note is published as soon as it is committed to the `master` branch.

### Jupyter Notebooks

Jupyter notebooks are converted to HTML with [nbconvert](https://nbconvert.readthedocs.io), using its `basic` template inside the `note.html` template. The first cell of the notebook must be a "raw" cell containing the front matter (in the same format as for Markdown files, including the `---` lines), and the second cell must be a Markdown cell with the title as a level-1 heading (`# Title`). The tag "notebook" is added automatically.

A notebook `foo.ipynb` is rendered to `foo/index.html`, so that its URL is `foo/`; a notebook `index.ipynb` is rendered to `index.html` in its folder. Images in the cell outputs are written as separate files into the same folder, and the original `.ipynb` file is copied there as well, so that readers can download it.

The notebooks are *not* executed during the build. The website shows the outputs as they are stored in the `.ipynb` file, so a notebook must be run and saved before it is committed.

To run the notebooks, use the `michaelgoerz-net` Jupyter kernel (display name "michaelgoerz.net"). It runs in the project's `.venv` environment, which includes the packages in the `notebooks` dependency group in `pyproject.toml` (NumPy, SciPy, matplotlib, pandas, statsmodels, SymPy). To add a package that a notebook needs, use `uv add --group notebooks <package>`.

* `make install-kernel` registers the kernel in the user's Jupyter installation.
* `make jupyter` registers the kernel and starts `jupyter notebook`. Jupyter itself is not part of the project environment: the `jupyter` command must be installed globally.
* `make uninstall-kernel` removes the kernel again.


## Deployment

The website is built and deployed by the GitHub Actions workflow in `.github/workflows/build.yml`. It runs on every push to any branch, and it can be started manually from the "Actions" tab of the repository on GitHub ("Run workflow").

The workflow installs uv and runs `make generate`. It sets `UV_LOCKED=1`, so the build fails if `uv.lock` is out of date with `pyproject.toml`, and `UV_NO_DEFAULT_GROUPS=1`, so that the `dev` and `notebooks` dependency groups are not installed.

On the `master` branch only, the workflow then uploads `output/` to `webserver.michaelgoerz.net` with `rsync` over SSH, as the user `goerz`, setting the group of all files to `www-data`. The private SSH key is stored in the repository secret `SSH_DEPLOY_KEY`. The server's host key is pinned in `.github/known_hosts`, which must be updated if the server's host key changes. On the server, the deploy key is restricted with `rrsync` to the web root, which is why the target directory in the workflow is `/`. The upload uses `--delete`, so files that are no longer generated are removed from the server. Pushes to other branches only check that the website builds.

Deployments never run concurrently: a push while a deployment is in progress waits for it to finish.


## Organization

The entries of the navigation bar are defined in `MENUITEMS` in `conf.py`. A page is shown as belonging to a menu entry through its `Section` front matter key. The social and contact links in the sidebar of the Research page and in the footer are defined in `SOCIAL`, `CONTACT`, and `FOOTER_CONTACT`.

When a published page moves, add its old path and its new URL to `REDIRECTS` in `conf_publish.py`, so that the old URL keeps working.


## Debugging

Run `uv run python generate.py --debug` to see debug output from the generator. This includes the list of ignored files, the template chosen for each file, the parsed front matter, and the rendered HTML of every page. The flag `--debug-all` additionally enables debug output from all libraries (markdown-it, nbconvert, …). Both flags can be combined with `--preview`. Warnings and errors are printed in red.

In preview mode, the generator checks once per second whether a Markdown or notebook file is newer than its output, and re-renders it if necessary. Changes to anything else are not picked up while the preview is running:

* new files
* static files (images, PDFs, …)
* templates, `theme/static/`, and `conf.py`
* the data files read by templates, like the `.bib` files for the Research page or `projects.yml` for the Programming page. A workaround is to `touch` the Markdown file of the page that reads the data, e.g., `touch content/index.md` after editing `content/research/papers.bib`.
* the Notes index, Tags, and Categories pages, when the title, date, or tags of a note change

In all of these cases, stop the preview with Ctrl-C and restart it.

The generator never deletes files from `output/` (except `output/theme/`). After renaming or deleting a source file, run `make clean` so that the stale output does not show up in the preview.

Run `make ipython` to start an IPython shell in the project environment, e.g., to test the Markdown parser interactively:

```python
from src.render_markdown import PARSER
print(PARSER.render("Some *markdown* with $x^2$"))
```

Run `make black` to format the Python code.


## Favicon

The favicon was generated with [favicon.io](https://favicon.io/favicon-generator/), using background color `#9495A0` and font IBM Plex Sans at size 80.


## License

The code in this repository is licensed under the [MIT](LICENSE) license. The *contents* of the website (anything in the [`content`](content) subfolder) under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/), if not indicated otherwise.
