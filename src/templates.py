"""Jinja 2 Template Management"""

import locale
import unicodedata
import re
from time import strftime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, BaseLoader

from .logging import LOG


def slugify(text):
    """Convert text into a "slug" that can be used in an URL.

    Slugs are lowercase ascii words separated with hyphens.
    """
    text = str(text)
    slug = (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    slug = re.sub(r"[^\w\s-]", "", slug.lower())
    slug = re.sub(r"[-_\s]+", "-", slug).strip("-")
    return slug


class DateFormatter:
    """A date formatter object used as a jinja filter"""

    def __init__(self):
        self.locale = locale.setlocale(locale.LC_TIME)

    def __call__(self, date, date_format):
        old_lc_time = locale.setlocale(locale.LC_TIME)
        old_lc_ctype = locale.setlocale(locale.LC_CTYPE)

        locale.setlocale(locale.LC_TIME, self.locale)
        # on OSX, encoding from LC_CTYPE determines the unicode output in PY3
        # make sure it's same as LC_TIME
        locale.setlocale(locale.LC_CTYPE, self.locale)

        formatted = strftime(date, date_format)

        locale.setlocale(locale.LC_TIME, old_lc_time)
        locale.setlocale(locale.LC_CTYPE, old_lc_ctype)
        return formatted


class Templates:
    """Template Manager."""

    def __init__(self, themefolder, defaults=()):

        simple_loader = FileSystemLoader(Path(themefolder) / "templates")
        self.env = Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            loader=simple_loader,
            extensions=[],
        )

        self._template_names = [
            name for name in self.env.list_templates() if "/" not in name
        ]
        LOG.info("Template list: %s", self._template_names)

        self.env.filters["strftime"] = DateFormatter()

        self.env.filters["slugify"] = slugify

        LOG.debug("Template list: %s", self.env.list_templates())

        # provide utils.strftime as a jinja filter
        self.env.filters.update({"strftime": DateFormatter()})

        self.defaults = defaults

    def keys(self):
        """Return a list of the available template names."""
        return list(self)

    def __len__(self):
        return len(self._template_names)

    def __getitem__(self, name):
        return self.env.get_template(name)

    def __iter__(self):
        return iter(self._template_names)

    def from_string(self, template_str):
        """Create a template directly from a string"""
        return self.env.from_string(template_str)

    def default_for(self, file, fallback=None):
        """Choose a template name for rendering the given file (Path)."""
        file = str(file)
        for (rx, template_name) in self.defaults:
            if rx.match(file):
                LOG.debug(
                    "Trying rx %r to find template for %r: Match -> %r",
                    rx,
                    str(file),
                    template_name,
                )
                return template_name
            else:
                LOG.debug(
                    "Trying rx %r to find template for %r: No Match",
                    rx,
                    str(file),
                )
        LOG.debug(
            "Returning fallback %r as default template for %r",
            fallback,
            str(file),
        )
        return fallback
